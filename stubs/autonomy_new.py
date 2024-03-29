import logging
from typing import List

from tilsdk import *                                            # import the SDK
from tilsdk.utilities import PIDController, SimpleMovingAverage # import optional useful things
# from tilsdk.mock_robomaster.robot import Robot                  # Use this for the simulator
from robomaster.robot import Robot                             # Use this for real robot

# Import your code
from cv_service import CVService, MockCVService
from nlp_service import NLPService
from planner import Planner
from utils_custom import *
import time

# Setup logging in a nice readable format
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)5s][%(asctime)s][%(name)s]: %(message)s',
                    datefmt='%H:%M:%S')

# Define config variables in an easily accessible location
# You may consider using a config file
REACHED_THRESHOLD_M = 0.3   # TODO: Participant may tune.
ANGLE_THRESHOLD_DEG = 20.0  # TODO: Participant may tune.
ROBOT_RADIUS_M = 0.17       # TODO: Participant may tune.

NLP_MODEL_DIR = '' # TODO: Participant to fill in.
# NLP_MODEL_DIR = 'saved_model_base-wav2vec2_large_xlsr_en_ser_ep-10_lr-5e-05_decay-1e-05_data-TIL_RAV_E1_E2_99'
CV_MODEL_DIR = 'yolov5l_img-1024_bs-8_ep-12_E1_E2_last.pt' # TODO: Participant to fill in.

# Convenience function to update locations of interest.
def update_locations(old:List[RealLocation], new:List[RealLocation]) -> None:
    '''Update locations with no duplicates.'''
    if new:
        for loc in new:
            if loc not in old:
                logging.getLogger('update_locations').info('New location of interest: {}'.format(loc))
                old.append(loc)

def main():
    # Initialize services
    cv_service = CVService(model_dir=CV_MODEL_DIR)
    # cv_service = MockCVService(model_dir=CV_MODEL_DIR)
    nlp_service = NLPService()
    loc_service = LocalizationService(host='192.168.20.56', port=5521)
    rep_service = ReportingService(host='localhost', port=5501)
    robot = Robot()
    robot.initialize(conn_type="sta", sn="3JKDH2T0014VYK")
    robot.camera.start_video_stream(display=False, resolution='720p')

    # Start the run
    rep_service.start_run()

    # Initialize planner
    map_:SignedDistanceGrid = loc_service.get_map()
    map_ = map_.dilated(1.5*ROBOT_RADIUS_M/map_.scale)
    
    print("Arena:")
    print(map_.grid.shape)
    print(convert_arena(map_.grid, False))

    planner = Planner(map_, sdf_weight=0.5)

    # Initialize variables
    seen_clues = set()
    curr_loi:RealLocation = None
    path:List[RealLocation] = []
    lois:List[RealLocation] = []
    curr_wp:RealLocation = None
    explored_grids:List[RealLocation] = []

    # Initialize tracker
    # TODO: Participant to tune PID controller values.
    tracker = PIDController(Kp=(0.0, 0.0), Kd=(0.0, 0.0), Ki=(0.0, 0.0))

    # Initialize pose filter
    pose_filter = SimpleMovingAverage(n=5)

    # Define filter function to exclude clues seen before   
    new_clues = lambda c: c.clue_id not in seen_clues

    # Main loop
    while True:
        # Get new data
        pose, clues = loc_service.get_pose()
        pose = pose_filter.update(pose)
        img = robot.camera.read_cv2_image(strategy='newest')
        
        if not pose:
            # no new data, continue to next iteration.
            continue

        # Filter out clues that were seen before
        clues = list(filter(new_clues, clues))
        print("all clues ", clues)
        
        # Process clues using NLP and determine any new locations of interest
        if clues:
            new_lois = nlp_service.locations_from_clues(clues)
            update_locations(lois, new_lois)
            seen_clues.update([c[0] for c in clues])
            print("seen clues ", seen_clues)

        # Process image and detect targets
        targets = cv_service.targets_from_image(img)

        # perform time.sleep to make sure the cv service is ready for the prediction
        time.sleep(4)

        # Submit targets
        if targets:
            logging.getLogger('Main').info('{} targets detected.'.format(len(targets)))
            logging.getLogger('Reporting').info(rep_service.report(pose, img, targets))
        
        if not curr_loi:
            if len(lois) == 0:
                logging.getLogger('Main').info('No more locations of interest.')
                # TODO: You ran out of LOIs. You could perform and random search for new
                # clues or targets
                break
            
            else:
                # Get new LOI
                lois.sort(key=lambda l: euclidean_distance(l, pose), reverse=True)
                curr_loi = lois.pop()
                logging.getLogger('Main').info('Current LOI set to: {}'.format(curr_loi))

                # Plan a path to the new LOI
                logging.getLogger('Main').info('Planning path to: {}'.format(curr_loi))
                path = planner.plan(pose[:2], curr_loi)

                # Add explored path of coordinates into explored coordinates
                explored_grids += path

                path.reverse() # reverse so closest wp is last so that pop() is cheap
                curr_wp = None
                logging.getLogger('Main').info('Path planned.')
        
        else:
            # There is a current LOI objective.
            # Continue with navigation along current path.
            if path:
                # Get next waypoint
                if not curr_wp:
                    curr_wp = path.pop()
                    logging.getLogger('Navigation').info('New waypoint: {}'.format(curr_wp))
                
                # Calculate distance and heading to waypoint
                dist_to_wp = euclidean_distance(pose, curr_wp)
                ang_to_wp = np.degrees(np.arctan2(curr_wp[1]-pose[1], curr_wp[0]-pose[0]))
                ang_diff = -(ang_to_wp - pose[2]) # body frame

                # ensure ang_diff is in [-180, 180]
                if ang_diff < -180:
                    ang_diff += 360

                if ang_diff > 180:
                    ang_diff -= 360

                logging.getLogger('Navigation').debug('ang_to_wp: {}, hdg: {}, ang_diff: {}'.format(ang_to_wp, pose[2], ang_diff))

                # Consider waypoint reached if within a threshold distance
                if dist_to_wp < REACHED_THRESHOLD_M:
                    logging.getLogger('Navigation').info('Reached wp: {}'.format(curr_wp))
                    tracker.reset()
                    curr_wp = None
                    continue
                
                # Determine velocity commands given distance and heading to waypoint
                vel_cmd = tracker.update((dist_to_wp, ang_diff))

                # reduce x velocity
                vel_cmd[0] *= np.cos(np.radians(ang_diff))
                
                # If robot is facing the wrong direction, turn to face waypoint first before
                # moving forward.
                if abs(ang_diff) > ANGLE_THRESHOLD_DEG:
                    vel_cmd[0] = 0.0
                
                # Send command to robot
                robot.chassis.drive_speed(x=vel_cmd[0], z=vel_cmd[1])
                
            else:
                logging.getLogger('Navigation').info('End of path.')
                curr_loi = None

                # TODO: Perform search behaviour? Participant to complete.

                continue

    robot.chassis.drive_speed(x=0.0, y=0.0, z=0.0)  # set stop for safety
    logging.getLogger('Main').info('Mission Terminated.')


if __name__ == '__main__':
    main()
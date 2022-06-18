import logging
from typing import List

from tilsdk import *                                            # import the SDK
from tilsdk.utilities import PIDController, SimpleMovingAverage # import optional useful things
# from tilsdk.mock_robomaster.robot import Robot                 # Use this for the simulator
from robomaster.robot import Robot                              # Use this for real robot

# Import your code
from cv_service import CVService, MockCVService
from nlp_service import NLPService
from planner import Planner
from a_star_algorithm import execute_astar

# Setup logging in a nice readable format
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)5s][%(asctime)s][%(name)s]: %(message)s',
                    datefmt='%H:%M:%S')

# Define config variables in an easily accessible location
# You may consider using a config file
REACHED_THRESHOLD_M = 0.3   # TODO: Participant may tune.
ANGLE_THRESHOLD_DEG = 20.0  # TODO: Participant may tune.
ROBOT_RADIUS_M = 0.17       # TODO: Participant may tune.
# NLP_MODEL_DIR = '/home/dh/Downloads/saved_model_base-wav2vec2_large_xlsr_en_ser_ep-10_lr-5e-05_decay-1e-05_data-TIL_RAV_E1_E2_99'          # TODO: Participant to fill in.
CV_MODEL_DIR = 'yolov5l_img-1024_bs-8_ep-12_E1_E2_last.pt'          # TODO: Participant to fill in.

def main():
    # Initialize services
    cv_service = CVService(model_dir=CV_MODEL_DIR)
    # cv_service = MockCVService(model_dir=CV_MODEL_DIR)
    # nlp_service = NLPService(model_dir=NLP_MODEL_DIR)
    nlp_service = NLPService()
    loc_service = LocalizationService(host='192.168.20.56', port=5521)
    rep_service = ReportingService(host='localhost', port=5501)
    robot = Robot()
    robot.initialize(conn_type="sta", sn="3JKDH2T0014VYK")
    robot.camera.start_video_stream(display=False, resolution='720p')

    # # Start the run
    # rep_service.start_run()

    # Initialize planner
    map_:SignedDistanceGrid = loc_service.get_map()
    print("lol jk")
    print(map_.grid)
    # TODO: process map?
    planner = Planner(map_, sdf_weight=0.5)

    print('plann', planner)

    # Initialize variables
    # TODO: If needed.

    # Initialize tracker
    # TODO: Participant to tune PID controller values.
    tracker = PIDController(Kp=(0.0, 0.0), Kd=(0.0, 0.0), Ki=(0.0, 0.0))

    # Main loop
    while True:
        # Get new data
        pose, clues = loc_service.get_pose()
        print('hello ', pose, clues)

        locations_from_clue = nlp_service.locations_from_clues(clues)
        print('morgan ', locations_from_clue)

        # after detection of the location, move the damn robot to the clue spot then perform obj detection

        img = robot.camera.read_cv2_image(strategy='newest')
        
        # TODO: Participant to complete.
        # pass the img to cv model
        classes_from_cv = cv_service.targets_from_image(img)
        print('hehe ', classes_from_cv)

        pass

    robot.chassis.drive_speed(x=0.0, y=0.0, z=0.0)  # set stop for safety
    logging.getLogger('Main').info('Mission Terminated.')


if __name__ == '__main__':
    main()
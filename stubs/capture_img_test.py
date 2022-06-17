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
from utils import *

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

    robot = Robot()
    robot.initialize(conn_type="sta", sn="3JKDH2T0014VYK")
    robot.camera.start_video_stream(display=False, resolution='720p')

    img = robot.camera.read_cv2_image(strategy='newest')

    # Process image and detect targets
    targets = cv_service.targets_from_image(img)

    print(targets)


if __name__ == '__main__':
    main()
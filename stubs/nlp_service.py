from typing import Iterable, List
from tilsdk.localization.types import *
import onnxruntime as ort
#from inference_asr import Evaluation
#import soundfile as sf
#from io import BytesIO

class NLPService:
    def __init__(self):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        
        # TODO: Participant to complete.
        # self.model_dir = model_dir
        pass

    def locations_from_clues(self, clues:Iterable[Clue]) -> List[RealLocation]:
        '''Process clues and get locations of interest.
        
        Parameters
        ----------
        clues
            Clues to process.

        Returns
        -------
        lois
            Locations of interest.
        '''

        # TODO: Participant to complete.

        # # initialise the pred list
        # #emotion_list = []

        # # initialise the locations list to store the dictionary of clue location if audio is classified under "distressed"
        # locations = []

        # # loop thru the list of Clue objects to do inference on all the audio bytes detected
        # for idx, clue_obj in enumerate(clues):

        #     # do the inference iteratively
        #     e = Evaluation(audio_file=BytesIO(clue_obj.audio), saved_model_dir=self.model_dir)
        #     pred_idx, emotion = e.predict()

        #     # classify the predicted emotions
        #     if emotion == 'angry' or emotion == 'sad':
        #         # emotion_class = 'distressed'
        #         locations.append(clue_obj.location)
        #     else:
        #         # emotion_class = 'not_distressed'
        #         continue

        #     # append the emotion class into the list
        #     #emotion_list.append(emotion_class)

        # return locations

        locations = [c.location for c in clues]

        return locations


class MockNLPService:
    '''Mock NLP Service.
    
    This is provided for testing purposes and should be replaced by your actual service implementation.
    '''

    def __init__(self, model_dir:str):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        pass

    def locations_from_clues(self, clues:Iterable[Clue]) -> List[RealLocation]:
        '''Process clues and get locations of interest.
        
        Mock returns location of all clues.
        '''
        locations = [c.location for c in clues]

        return locations
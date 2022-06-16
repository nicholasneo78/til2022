from typing import List, Any
from tilsdk.cv.types import *
import onnxruntime as ort
from inference_cv import InferenceCV

class CVService:
    def __init__(self, model_dir):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''

        # TODO: Participant to complete.
        self.model_dir = model_dir

    def targets_from_image(self, img) -> List[DetectedObject]:
        '''Process image and return targets.
        
        Parameters
        ----------
        img : Any
            Input image.
        
        Returns
        -------
        results  : List[DetectedObject]
            Detected targets.
        '''
        
        # TODO: Participant to complete.

        # call the inference class to get the InferenceCV object
        infer = InferenceCV(model_path=self.model_dir, 
                            img=img, 
                            img_width=1280,
                            img_height=720,
                            img_is_pixel=True)

        get_coords = infer()

        if len(get_coords) == 0:
            return []

        detected_list = []

        # store the bounding box
        for box in get_coords:
            bbox = BoundingBox(box[1], box[2], box[3], box[4])
            obj = DetectedObject(img_id, box[0], bbox)
            detected_list.append(obj)

        return detected_list

class MockCVService:
    '''Mock CV Service.
    
    This is provided for testing purposes and should be replaced by your actual service implementation.
    '''

    def __init__(self, model_dir:str):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        # Does nothing.
        pass

    def targets_from_image(self, img:Any) -> List[DetectedObject]:
        '''Process image and return targets.
        
        Parameters
        ----------
        img : Any
            Input image.
        
        Returns
        -------
        results  : List[DetectedObject]
            Detected targets.
        '''
        # dummy data
        bbox = BoundingBox(100,100,300,50)
        obj = DetectedObject("1", "1", bbox)
        return [obj]
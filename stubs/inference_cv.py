import numpy as np
import cv2
from PIL import Image

# PyTorch Hub
import torch

class InferenceCV:
    def __init__(self, model_path, img, img_width, img_height, img_is_pixel=True):
        self.model_path = model_path
        self.img = img
        self.img_width = img_width
        self.img_height = img_height
        self.img_is_pixel = img_is_pixel

    def inference(self):
        model = torch.hub.load('../yolov5/', 'custom', path=self.model_path, force_reload=False, source='local')

        # self.img is not an array of pixels but an img path to an image
        if not self.img_is_pixel:
            process = cv2.imread(self.img)
            results = model(process)

        # self.img is an array of pixels
        else:
            results = model(self.img)
        
        labels, cord_thres = results.xyxyn[0][:, -1].tolist(), results.xyxyn[0][:, :-1]

        # initialise a list to store each bbox details
        label_coord_list = []

        for idx in range(len(labels)):
            # preprocess to get the coco format values
            x_start = results.xyxyn[0][:, :-1][idx].tolist()[0]
            y_start = results.xyxyn[0][:, :-1][idx].tolist()[1]
            x_end = results.xyxyn[0][:, :-1][idx].tolist()[2]
            y_end = results.xyxyn[0][:, :-1][idx].tolist()[3]

            # get x, y, w, h
            x = round(self.img_width*(x_end+x_start)/2, 4)
            y = round(self.img_height*(y_end+y_start)/2, 4)
            w = round(self.img_width*(x_end-x_start), 4)
            h = round(self.img_height*(y_end-y_start), 4)

            # according to the competition where '1' is fallen and '0' is standing
            if str(int(labels[idx])) == '1':
                relabel = '1'
            else:
                relabel = '0'

            label_coord = [relabel, x, y, w, h]
            label_coord_list.append(label_coord)

        # to show the image with the bbox
        # results.show()

        return label_coord_list

    def __call__(self):
        return self.inference()

infer = InferenceCV(model_path='yolov5l_img-1024_bs-8_ep-12_E1_E2_last.pt', 
                    img='/home/daniel/Desktop/til2022/data/imgs/1.jpg', 
                    img_width=1280,
                    img_height=720,
                    img_is_pixel=False)

get_coords = infer()
print(get_coords)
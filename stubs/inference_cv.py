import numpy as np
import cv2
from PIL import Image

# PyTorch Hub
import torch

class InferenceCV:
    def __init__(self, model_path, img, img_width, img_height):
        self.model_path = model_path
        self.img = img
        self.img_width = img_width
        self.img_height = img_height

    def inference(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path, force_reload=False)

        results = model(self.img)

        labels, cord_thres = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        # initialise a list to store each bbox details
        label_coord_list = []

        for idx in range(len(labels)):
            # preprocess to get the coco format values
            x_start = results.xyxyn[0][:, :-1][idx].tolist()[0]
            y_start = results.xyxyn[0][:, :-1][idx].tolist()[1]
            x_end = results.xyxyn[0][:, :-1][idx].tolist()[2]
            y_end = results.xyxyn[0][:, :-1][idx].tolist()[3]

            # get x, y, w, h
            x = self.img_width*(x_end+x_start)/2
            y = self.img_height*(y_end+y_start)/2
            w = self.img_width*(x_end-x_start)
            h = self.img_height*(y_end-y_start)

            label_coord = [labels, x, y, w, h]
            label_coord_list.append(label_coord)

            results.show()

            return label_coord_list

    def __call__(self):
        return self.inference()

infer = InferenceCV(model_path='yolov5l_img-1024_bs-8_ep-12_E1_E2_last.pt', 
                    img='/home/daniel/Desktop/til2022/data/imgs/1.jpg', 
                    img_width=1280,
                    img_height=720)

get_coords = infer()
print(get_coords)

# print(labels)
# print()
# print(cord_thres)
# print()
# print(results)
# print(results.xyxyn[0][:, :-1][1].tolist())





# # print(x, y, w, h, labels.tolist()[0])
# print(labels, cord_thres)

# results.show()

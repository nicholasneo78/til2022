import cv2 as cv
import numpy as np

import numpy as np
import cv2
from PIL import Image

# PyTorch Hub
import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5l_img-1024_bs-8_ep-12_E1_E2_last.pt', force_reload=False)

img = '/home/daniel/Desktop/til2022/data/imgs/fallen_person.jpeg'

results = model(img)

labels, cord_thres = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()

print(labels)
print()
print(cord_thres)

# Morphological Transformations

import cv2 as cv
import numpy as np
import os
#from util import utils

def contour_detection(path, image, file_type):
    img_color = cv.imread(f'{path}/{image}.{file_type}')
    img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
    ret, img_binary = cv.threshold(img_gray, 100, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 3)  # blue

    cv.imwrite(f'contours/{file}.{file_type}', img_color)
    
    for cnt in contours:
        area = cv.contourArea(cnt)

    print(area)

test_image_path = "images"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
#files = [('198300007', 'jpg'), ('198300049', 'jpg'), ('198300064', 'jpg'), ('198300091', 'jpg'),('drug_image', 'jpeg'),\
#         ('200711918', 'jpg'), ('cuba', 'png'), ('test1', 'png'), ('test2', 'png'), ('test3', 'png'), ('test4', 'png'),\
#         ('threshold', 'png')]
    
for file, file_type in files:
    print(f"{file}.{file_type}")
    contour_detection(test_image_path, file, file_type)
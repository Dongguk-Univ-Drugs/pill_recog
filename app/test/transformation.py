# Morphological Transformations

import cv2
import numpy as np
import os
#from util import utils

def edge_detection(path, image, file_type):
    img = cv2.imread(f'{path}/{image}.{file_type}', cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread('image1.png', cv2.IMREAD_GRAYSCALE)

    # robertsx = np.array([[-1,0,0], [0,1,0], [0,0,0]])
    # robertsy = np.array([[0,0,-1], [0,1,0], [0,0,0]])


    # sobelX = cv2.Sobel(img, -1, 1, 0, ksize=3)
    # sobelY = cv2.Sobel(img, -1, 0, 1, ksize=3)
    # sobel = sobelX + sobelY
    # cv2.imwrite('transformation/sobel.png', sobel)

    #blur = cv2.medianBlur(img, 5)
    blur = cv2.GaussianBlur(img, (7,7), 0)
    # cv2.imwrite('transformation/blur.png', blur)

    #ret, threshold = cv2.threshold(blur, 127, 255, 1)
    #threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C  , cv2.THRESH_BINARY, 11, 2)
    # threshold = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #cv2.imwrite(f'transformation/{image}_threshold.png', threshold)

    #canny = cv2.Canny(threshold, 50, 100)
    canny = cv2.Canny(blur, 40, 180)
    cv2.imwrite(f'transformation/{image}_canny.png', canny)

    # kernel = np.ones((5,5),np.uint8)
    # erosion = cv2.erode(canny, kernel,iterations = 1)
    # cv2.imwrite('transformation/erosion.png', erosion)

    # dilation = cv2.dilate(canny, kernel,iterations = 1)
    # cv2.imwrite('transformation/dilation.png', dilation)

    # opening = cv2.morphologyEx(canny, cv2.MORPH_OPEN, kernel)
    # cv2.imwrite('transformation/opening.png', opening)

test_image_path = "circle"
#test_image_path = "saliency"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

for file, file_type in files:
    print(f"{file}.{file_type}")
    edge_detection(test_image_path, file, file_type)
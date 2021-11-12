import cv2
import os
import numpy as np

#test_image_path = "area/result"
test_image_path = "saliency"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

for file, file_type in files:
    print(f"{file}.{file_type}")
    
    img = cv2.imread(f"{test_image_path}/{file}.{file_type}", cv2.IMREAD_GRAYSCALE)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #gaussianblur = cv2.GaussianBlur(img, (7,7), 0)
    #threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C  , cv2.THRESH_BINARY, 11, 1)
    ret, threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cv2.imwrite(f"binary/{file}.{file_type}", threshold)

    #reader = easyocr.Reader(['en'], gpu=False)
    #result = reader.readtext(f'{test_image_path}/{file}.{file_type}')



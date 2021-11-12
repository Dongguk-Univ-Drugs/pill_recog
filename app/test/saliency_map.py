import cv2
import numpy as np
import os

def saliency_map(path, file, file_type):
    image = cv2.imread(f"{path}/{file}.{file_type}", cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (7,7), 0)

    # 우리 코드의 핵심 cv2를 이용해 Sailencymap을 계산
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(image)
    saliencyMap = (saliencyMap * 200).astype("uint8") # 0-1 사이의 값을 0-255의 값으로
    cv2.imwrite(f"saliency/{file}.png", saliencyMap)

    # thre saliency map에 추가적으로 threshold 과정을 넣어준다.
    #threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_OTSU)[1]
    #cv2.imwrite(f"threshold/{file}_thresholdMap.png", threshMap) # 비교를 위해 저장

    
#test_image_path = "area/result"
test_image_path = "circle"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

for file, file_type in files:
    print(f"{file}.{file_type}")
    saliency_map(test_image_path, file, file_type)

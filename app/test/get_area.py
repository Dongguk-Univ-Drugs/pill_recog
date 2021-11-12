import cv2
import numpy as np
import os
"""

"""

def applyPadding(length):
    if length>3000:
        padding = int(length/10/2)
    else:
        padding = 0
    return padding, length-padding

def getarea(path, file, file_type):
    # step1 - 물체의 주변부 찾기
    # : param image : 물체의 찾을 사진의 이미지
    # : return res : 찾아낸 물체 사진

    image = cv2.imread(f"{path}/{file}.{file_type}", cv2.IMREAD_GRAYSCALE)

    # 원본 이미지 사진 크기 재조정 할일이 있을 경우 사용
    imageHeight, imageWidth = image.shape[:2]

    width, height = image.shape
    s_width, e_width = applyPadding(width)
    s_height, e_height = applyPadding(height)
    resizeImage = image[s_width:e_width, s_height:e_height]

    # 우리 코드의 핵심 cv2를 이용해 Sailencymap을 계산
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(resizeImage)
    saliencyMap = (saliencyMap * 255).astype("uint8") # 0-1 사이의 값을 0-255의 값으로
    cv2.imwrite(f"area/{file}.png", saliencyMap) # 비교를 위해 저장

    # thre saliency map에 추가적으로 threshold 과정을 넣어준다.
    threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_OTSU)[1]
    #cv2.imwrite(f"area/{file}_thresholdMap.png", threshMap) # 비교를 위해 저장

    contours, hierachy = cv2.findContours(threshMap, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    area, output = 0, contours[0]

    for cnt in contours:
        if area < cv2.contourArea(cnt):
            area = cv2.contourArea(cnt)
            output = cnt

    # 근사치 구하기
    epsilon = 0.03 * cv2.arcLength(output, True)
    approx = cv2.approxPolyDP(output, epsilon, True)

    # 찾은 물체의 근사치 좌표 구하기
    x, y, w, h = cv2.boundingRect(approx)
    rx = x-100 if x>100 else 0
    ry = y-100 if y>100 else 0
    if x>40:
        rx = x-40
    if y>100:
        ry = y-100

    print(f"width : {width}, height : {height} and rx : {rx}, x+w+100 : {x+w+100} , ry : {ry} y+h+100 : {y+h+100}")
    # 사진 자르기
    dst = resizeImage[ry:y+h+100, rx:x+w+100]
    cv2.imwrite(f"area/result/{file}.png", dst) # 최종
    return dst

    
test_image_path = "images"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

for file, file_type in files:
    print(f"{file}.{file_type}", end=" : ")
    coordinates = getarea(test_image_path, file, file_type)

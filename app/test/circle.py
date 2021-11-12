import cv2
import numpy as np
import os
import math

def key_close_from_middle(point):
    print(f"{middle} : {point}")
    x = middle[0]-point[0][0]
    y = middle[1]-point[0][1]
    return math.sqrt(x*x+y*y)

test_image_path = "area/result"
files = [(file.split('.')[0],file.split('.')[1])for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
files.sort()
for file, file_type in files:
    img = cv2.imread(f'{test_image_path}/{file}.{file_type}', 0)
    mask = np.zeros_like(img)
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    height, width, type = cimg.shape
    minradius = int(min(height/3, width/3))
    maxradius = int(max(height/2, width/2))

    middle = (int(width/2), int(height/2))
    middle_width = int(width/2)
    middle_height = int(height/2)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT, 1, minradius, param1=50,param2=30,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # 중심에서 가장 가까운 순서로 정렬
        sorted(circles, key=key_close_from_middle)
        for indx, i in enumerate(circles[0,:]):
            if middle_width-100<=i[1] and i[1]<=middle_width+100 and\
               middle_height-100<=i[0] and i[0]<=middle_height+100:
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.circle(mask,(i[0],i[1]),i[2],(255,255,255),-1)
                masked = cv2.bitwise_and(img, mask)
                cv2.imwrite(f'circle/{file}.png', masked)
                break   
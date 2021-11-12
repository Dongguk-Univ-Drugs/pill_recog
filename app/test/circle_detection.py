import cv2
import numpy as np
import os
import math

def onChange(x):
    pass

def key_close_from_middle(point):
    x = middle[0]-point[0][0]
    y = middle[1]-point[0][1]
    return math.sqrt(x*x+y*y)

img = cv2.imread('result/image1.png', cv2.IMREAD_GRAYSCALE)
height, width = img.shape
minradius = int(min(height/3, width/3))
#cv2.namedWindow('circle detection')
#cv2.imshow('circle detection', img)
parameter1 = 1
parameter2 = 1
mask = np.zeros_like(img)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

height, width, type = cimg.shape
minradius = int(min(height/3, width/3))
maxradius = int(max(height/2, width/2))

middle = (int(width/2), int(height/2))
middle_width = int(width/2)
middle_height = int(height/2)
while True:
    copy_img = img.copy()
    print(f"parameter1:{parameter1} parameter2:{parameter2}")
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT, 1, minradius, param1=parameter1,param2=parameter2,minRadius=0,maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"len : {len(circles)}")
        # 중심에서 가장 가까운 순서로 정렬
        sorted(circles, key=key_close_from_middle)
        for indx, i in enumerate(circles[0,:]):
            if middle_width-100<=i[1] and i[1]<=middle_width+100 and\
               middle_height-100<=i[0] and i[0]<=middle_height+100:
                #cv2.circle(copy_img,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.circle(mask,(i[0],i[1]),i[2],(255,255,255),-1)
                masked = cv2.bitwise_and(copy_img, mask)
        cv2.imwrite(f'circle/image1_{parameter1}_{parameter2}.png', masked)
        #cv2.imshow('circle detection', masked)
    if parameter2<30:
        parameter2+=1
    elif parameter2==30:
        parameter1+=1
        parameter2=1
    elif parameter1==51:
        break

#cv2.destroyAllWindows()

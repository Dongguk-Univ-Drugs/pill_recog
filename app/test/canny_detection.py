import cv2
import numpy as np
import os

def onChange(x):
    pass

img = cv2.imread('result/image16.png', cv2.IMREAD_GRAYSCALE)
cv2.namedWindow('edge detection')

cv2.createTrackbar('low threshold', 'edge detection', 0, 255, onChange)
cv2.createTrackbar('high threshold', 'edge detection', 0, 255, onChange)
cv2.imshow('edge detection', img)

while True:
    k = cv2.waitKey(20) & 0xFF
    print(k)
    if k == 27:
        break

    low = cv2.getTrackbarPos('low threshold', 'edge detection')
    high = cv2.getTrackbarPos('high threshold', 'edge detection')
    print(f"{low} ~ {high}")
    if low > high:
        print("Low threshold must be low than high threshold")
    elif ((low==0) and (high==0)):
        cv2.imshow('edge detection', img)
    else:
        canny = cv2.Canny(img, low, high)
        cv2.imshow('edge detection', canny)
    
cv2.destroyAllWindows()

# blur = cv2.GaussianBlur(img, (7,7), 0)
# canny = cv2.Canny(blur, 50, 200)
# cv2.imshow('edge detection', canny)

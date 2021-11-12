import cv2
import numpy as np
import imutils

# read image from disk
#image = cv2.imread('196200046.png')
image = cv2.imread('yjp.png')
# make it gray
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('test_ocr_cvt.png', img)

# blur it to remove noise
img = cv2.GaussianBlur(img, (7,7), 0)
cv2.imwrite('test_ocr_gaussian.png', img)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(img, 10, 100)
dilate = cv2.dilate(edged, None, iterations=2)
cv2.imwrite('test_ocr_canny.png', dilate)
# perform erosion if necessay, it completely depends on the image
# erode = cv2.erode(dilate, None, iterations=1)

# create an empty masks
mask = np.ones(img.shape[:2], dtype="uint8") * 255

# find contours
cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

orig = img.copy()
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 300:
        cv2.drawContours(mask, [c], -1, 0, -1)
    
    x,y,w,h = cv2.boundingRect(c)
    
    # filter more contours if nessesary
    if(w>h):
        cv2.drawContours(mask, [c], -1, 0, -1)
    
newimage = cv2.bitwise_and(dilate.copy(), dilate.copy(), mask=mask)
img2 = cv2.dilate(newimage, None, iterations=3)
ret2, th1 = cv2.threshold(img2 ,0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

print(th1)
cv2.imwrite('test_ocr.png', th1)

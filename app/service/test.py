import cv2
from preprocessing import Preprocessing

pp = Preprocessing()

img_path = '../test/test4.png'

img = cv2.imread(img_path)
img = pp.remove_noise(img)
gray = pp.get_grayscale(img)
# dilated = pp.dilate(gray)
# cannyed = pp.canny(dilated)
# thres = pp.thresholding(dilated)

cv2.imshow("test", gray)
cv2.waitKey(0)
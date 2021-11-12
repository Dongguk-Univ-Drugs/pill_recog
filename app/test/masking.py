import numpy as np, cv2
import matplotlib.pylab as plt

#--① 이미지 읽기
img = cv2.imread('area/result/image7.png')

#--② 마스크 만들기
mask = np.zeros_like(img)
cv2.circle(mask, (260,210), 100, (255,255,255), -1)
#cv2.circle(대상이미지, (원점x, 원점y), 반지름, (색상), 채우기)

#--③ 마스킹
masked = cv2.bitwise_and(img, mask)

#--④ 결과 출력
cv2.imwrite('masking/original.png', img)
cv2.imwrite('masking/mask.png', mask)
cv2.imwrite('masking/masked.png', masked)

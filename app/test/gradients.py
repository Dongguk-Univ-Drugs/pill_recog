import cv2
import os
import numpy as np

def edge_detection(path, image, file_type):
    path = f'{path}/{image}.{file_type}'
    print(f'{path}')
    img = cv2.imread(f'{path}', cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (7,7), 0)
    # roberts는 제외
    # robertsx = np.array([[-1, 0], [0, 1]])
    # robertsy = np.array([[0, -1], [1, 0]])
    # robertsX = cv2.filter2D(img, cv2.CV_64F, robertsx)
    # robertsY = cv2.filter2D(img, cv2.CV_64F, robertsy)
    # roberts = robertsX + robertsY
    # cv2.imwrite(f'gradients/{image}_roberts.png', roberts)

    prewittx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewitty = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    prewitt_ = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
    prewittX = cv2.filter2D(img, -1, prewittx)
    prewittY = cv2.filter2D(img, -1, prewitty)
    prewitt_ = cv2.filter2D(img, -1, prewitt_)
    # prewiitX,Y 도 제외
    #cv2.imwrite(f'gradients/{image}_prewittX.png', prewittX)
    #cv2.imwrite(f'gradients/{image}_prewittY.png', prewittY)
    #cv2.imwrite(f'gradients/{image}_prewitt_.png', prewitt_)


    sobelX = cv2.Sobel(img, -1, 1, 0, ksize=3)
    sobelY = cv2.Sobel(img, -1, 0, 1, ksize=3)
    sobel = sobelX + sobelY
    # sobelx = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
    # sobely = cv.Sobel(img,cv.CV_64F,0,1,ksize=5)
    cv2.imwrite(f'gradients/{image}_sobelX.png', sobelX)
    cv2.imwrite(f'gradients/{image}_sobelY.png', sobelY)
    cv2.imwrite(f'gradients/{image}_sobel.png', sobel)

    scharrX = cv2.Sobel(img, -1, 1, 0, ksize=cv2.FILTER_SCHARR)
    scharrY = cv2.Sobel(img, -1, 0, 1, ksize=-1)
    scharr = scharrX + scharrY
    cv2.imwrite(f'gradients/{image}_scharr.png', scharr)

#test_image_path = "area/result"
test_image_path = "images"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

for file, file_type in files:
    print(f"{file}.{file_type}")
    edge_detection(test_image_path, file, file_type)
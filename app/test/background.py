import cv2
import numpy as np
import os

def background(path, file, file_type):
    # 이미지 불러오기
    img = cv2.imread(f'{path}/{file}.{file_type}')

    # 변환 graky
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 임계값 조절
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # mask
    mask = 255 - mask

    # morphology 적용
    # borderconstant 사용
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # 저장
    cv2.imwrite('background/{image}.png', result)

test_image_path = "result"
#test_image_path = "saliency"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
# files = [('198300007', 'jpg'), ('198300049', 'jpg'), ('198300064', 'jpg'), ('198300091', 'jpg'),\
#          ('200711918', 'jpg'), ('cuba', 'png'), ('test1', 'png'), ('test2', 'png'), ('test3', 'png'), ('test4', 'png')]
    
for file, file_type in files:
    print(f"{file}.{file_type}")
    background(test_image_path, file, file_type)
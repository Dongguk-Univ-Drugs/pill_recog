import numpy as np
import cv2
import math

"""the class of Preprocessing which takes before predicting text, color, shape and divider
As seeing the step of @Jungin's code, the steps will be like below

- GaussianBlur
- Get Contour and create Foreground image
- Convert Color to gray and create Gray Foreground image
- create CLAHE method and create Clahe Foreground from Gray Foreground
- Create Threshold from Clahe Foreground
- Close Image (DON'T KNOW)
- Get Bounding Rectangle?
- Use Canny Edge from Gray Foreground
- Get threshold from Canny Edge 
- Get Hough line using thresh
"""

def get_foreground(img) -> np.ndarray:
    # pre-process before getting out of foreground
    gaussian_blured = cv2.GaussianBlur(img, (7, 7), 0)
    masked = np.zeros(gaussian_blured.shape[:2], np.uint8)
    # TODO: WHY ITS SAME MODEL?
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    # get width and height
    width, height = gaussian_blured.shape[1], gaussian_blured.shape[0]
    # get end points, int(width * 0.9) ==? width - (width // 10)
    end_x, end_y = int(width * 0.9), int(height * 0.9)
    # get rectangle from width, height and end of x and y in tuple
    width_tp = width // 10
    height_tp = height // 10
    rect = (width_tp, height_tp, end_x - width_tp, end_y - height_tp)
    # make grabcut for foreground
    # TODO: NO RETURN ..? WHY
    # img, mask, rect, bgdModel, fgdModel, iterCount, mode
    cv2.grabCut(img, masked, rect, bgd_model, fgd_model, 7,
                cv2.GC_INIT_WITH_RECT)
    # get newly masked
    new_masked = np.where((masked == 2) | (masked == 0), 0,
                            1).astype('uint8')
    result = img * new_masked[:, :, np.newaxis]

    return result

def create_img_for_text_recognition(img):
    """process for SHAPE recognition

    Args:
        img (numpy.ndarray): the result data from `get_foreground`
    """
    # create gray_foreground image first
    grayscale_fgd = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # TODO: NO IDEA WITH CLAHE WORKS
    # clahe = cv2.createCLAHE(4.0, (8, 8))
    # clahe_fgd = clahe.apply(grayscale_fgd)
    # clahe_retval, clahe_threshold = cv2.threshold(clahe_fgd, 110, 255, cv2.THRESH_BINARY)
    # # erode and dilate
    # kernal = np.ones((3, 3), np.uint8)
    # eroded_img = cv2.erode(clahe_threshold, kernal)
    # dilated_img = cv2.dilate(eroded_img, kernal)

    canny_edged_img = cv2.Canny(grayscale_fgd, 40, 150)
    canny_retval, canny_thres_img = cv2.threshold(canny_edged_img, 110,
                                                    255, cv2.THRESH_BINARY)
    return canny_thres_img

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255,
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # return cv2.threshold(image, 110, 255, cv2.THRESH_BINARY)[1]

#dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

#erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image,
                                M, (w, h),
                                flags=cv2.INTER_CUBIC,
                                borderMode=cv2.BORDER_REPLICATE)
    return rotated

def is_under_color_range(image, low, high):
    img_height, img_width, img_channel = image.shape
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    image_hsv = cv2.inRange(image_hsv, low, high)

    # 필요하면 주석 제거
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    mask = cv2.dilate(image_hsv, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    mask = cv2.erode(mask, kernel)

    contours, hierarchy = cv2.findContours(image_hsv, cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        min_value = min(img_height, img_width) * img_channel * 10
        max_value = img_height * img_width
        if min_value < area < max_value:
            return True
    return False

# if photo taken by camera, assume width and height are greater than 3000
def apply_padding(size):
    if size>3000:
        padding = int(size/10/2)
    else:
        padding = 0
    return padding, size-padding

# get object(drug) area and crop it.
def get_object_area(image):
    width, height = image.shape
    s_width, e_width = apply_padding(width)
    s_height, e_height = apply_padding(height)
    resize_image = image[s_width:e_width, s_height:e_height]

    # 우리 코드의 핵심 cv2를 이용해 Sailencymap을 계산
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(resize_image)
    saliencyMap = (saliencyMap * 255).astype("uint8") # 0-1 사이의 값을 0-255의 값으로
    threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_OTSU)[1]

    contours, hierachy = cv2.findContours(threshMap, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    area, output = 0, contours[0]

    for cnt in contours:
        if area < cv2.contourArea(cnt):
            area = cv2.contourArea(cnt)
            output = cnt

    # get approximation of object
    epsilon = 0.03 * cv2.arcLength(output, True)
    approx = cv2.approxPolyDP(output, epsilon, True)

    # get coordinates of found object.
    x, y, w, h = cv2.boundingRect(approx)
    rx = x-100 if x>100 else 0
    ry = y-100 if y>100 else 0

    # crop
    result = resize_image[ry:y+h+100, rx:x+w+100]
    return result

def get_circles(image):
    #img = cv2.GaussianBlur(image, (0, 0), 1)
    img = cv2.medianBlur(image, 5)
    #cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #height, width, type = cimg.shape
    height, width = img.shape
    minradius = int(min(height/3, width/3))
    maxradius = int(max(height/2, width/2))
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, \
                               minradius, param1=50, param2=30,\
                               minRadius=0,maxRadius=0)
    return circles

def get_circle_area(image, circles):
    def key_by_close_from_middle(point):
        x = middle[0]-point[0][0]
        y = middle[1]-point[0][1]
        return math.sqrt(x*x+y*y)
    mask = np.zeros_like(image)
    img = cv2.medianBlur(image, 5)

    height, width = img.shape
    middle = (int(width/2), int(height/2))
    middle_width = int(width/2)
    middle_height = int(height/2)

    circles = np.uint16(np.around(circles))
    # 중심에서 가장 가까운 순서로 정렬해서 가장 가까운 원만 포함
    sorted(circles, key=key_by_close_from_middle)
    for circle in circles[0,:]:
        x, y, r = circle[1], circle[0], circle[2]
        if middle_width-100<=x and x<=middle_width+100 and\
            middle_height-100<=y and y<=middle_height+100:
            cv2.circle(mask, (y,x), r, (255,255,255), -1)
            masked = cv2.bitwise_and(img, mask)
            return masked
    return image
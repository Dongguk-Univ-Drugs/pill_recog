import numpy as np
import cv2
import sys


def getPillContour(src):
    mask = np.zeros(src.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    width = src.shape[1]
    height = src.shape[0]
    endx = width - (width // 10)
    endy = height - (height // 10)
    rect = (width//10, height//10, endx-width//10, endy-height//10)

    cv2.grabCut(src, mask, rect, bgdModel, fgdModel, 7, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    src = src*mask2[:, :, np.newaxis]

    return src


def closing(src):
    kernel = np.ones((3, 3), np.uint8)
    result = cv2.dilate(src, kernel)
    result = cv2.erode(result, kernel)
    return result


def opening(src):
    kernel = np.ones((3, 3), np.uint8)
    result = cv2.erode(src, kernel)
    result = cv2.dilate(result, kernel)
    return result


def get_houghline(src, edges):
    lines = cv2.HoughLines(edges, 1, np.pi/180, 110)

    for i in range(len(lines)):
        for rho, theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0+1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return src, lines


def dividerDetector(src, boundRect, lines):
    x, y, w, h = boundRect
    center = ((x + (x+w)) // 2, (y+(y+h)) // 2)


if __name__ == "__main__":
    src = cv2.imread('../images/aa.jpg')
    if src is None:
        print('Image load failed!')
        sys.exit()
    image = cv2.GaussianBlur(src, (7, 7), 0)

    foreground = getPillContour(image)
    cv2.imshow("foreground", foreground)
    gray_foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    clahe_foreground = clahe.apply(gray_foreground)
    ret, img_threshold = cv2.threshold(
        clahe_foreground, 100, 255, cv2.THRESH_BINARY)

    closing_image = closing(img_threshold)
    boundR = cv2.boundingRect(closing_image)

    canny = cv2.Canny(gray_foreground, 40, 150)
    ret, thresh = cv2.threshold(canny, 100, 255, cv2.THRESH_BINARY)

    # thresh = closing(thresh)
    # thresh = opening(thresh)
    cv2.imshow("Trhe", thresh)

    cv2.imshow("canny", canny)

    hough, lines = get_houghline(src, thresh)
    print("[ Divider Detector ]", lines)
    dividerDetector(hough, boundR, lines)
    cv2.waitKey(0)
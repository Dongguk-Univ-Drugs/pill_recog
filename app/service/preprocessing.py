import numpy as np
import cv2


class Preprocessing:
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
    def create_cv2_mode(self, uploaded_byte) -> np.ndarray:
        """make uploaded file to be useful for opencv-python

        Args:
            uploaded_byte (UploadedFile): input image from client

        Returns:
            [numpy.ndarray]: the result of image with `numpy`
        """
        encoded_img = np.fromstring(uploaded_byte, dtype=np.uint8)
        src = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        return src

    def get_foreground(self, img) -> np.ndarray:
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

    def create_img_for_text_recognition(self, img):
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
    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image, 5)

    #thresholding
    def thresholding(self, image):
        # return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return cv2.threshold(image, 110, 255, cv2.THRESH_BINARY)[1]

    #dilation
    def dilate(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    #erosion
    def erode(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    #opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    #canny edge detection
    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    #skew correction
    def deskew(self, image):
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

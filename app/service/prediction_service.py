# custom path
import cv2
from service.load import Reference
from service.preprocessing import Preprocessing

# use Tesseract
import pytesseract
from pytesseract import Output

# TODO; has to be Singleton
class PredictionService:
    def __init__(self):
        """init from different classes
        - Preprocessing
        - Reference
        """
        self.ref = Reference()
        self.preprocess = Preprocessing()

    def get_color_group(self, img):
        """use Foreground of image to distribute the group of color

        Args:
            img (numpy.ndarray): result data from Preprocessing.get_foreground
        """
        pass

    def get_shape(self, img):
        '''
        Place Jungin's code here
        '''
        pass

    def get_divider(self, img):
        '''
        Place Jungin's code here
        '''
        pass

    def get_text(self, img):
        """get option from user and return value by its option

        Args:
            img (UploadedFile): the image data which has uploaded from client
            opt (int): the option will take whether to change the origin data to what
        """
        pp = self.preprocess
        # # get img converted to cv2 mode
        converted_img = pp.create_cv2_mode(img)
        # # get preprocessed img from preprocessing
        # foreground_img = pp.get_foreground(converted_img)
        # preprocessed_img = pp.create_img_for_text_recognition(foreground_img)
        gray_scaled_img = pp.get_grayscale(converted_img)
        # dilated_img = pp.dilate(gray_scaled_img)
        # thresholding_img = pp.thresholding(gray_scaled_img)
        # use Tesseract to recognize the text
        text_recog_result = pytesseract.image_to_data(gray_scaled_img,
                                                      nice=0,
                                                      output_type=Output.DICT)
        return text_recog_result['text']

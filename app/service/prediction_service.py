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
        thresholding_img = pp.thresholding(gray_scaled_img)
        # use Tesseract to recognize the text
        """pytesseract controls
        --oem : OCR Engine modes:
        0    Legacy engine only.
        1    Neural nets LSTM engine only.
        2    Legacy + LSTM engines.
        3    Default, based on what is available.
        
        --psm : Page Segmentation modes:
        0    Orientation and script detection (OSD) only.
        1    Automatic page segmentation with OSD.
        2    Automatic page segmentation, but no OSD, or OCR.
        3    Fully automatic page segmentation, but no OSD. (Default)
        4    Assume a single column of text of variable sizes.
        5    Assume a single uniform block of vertically aligned text.
        6    Assume a single uniform block of text.
        7    Treat the image as a single text line.
        8    Treat the image as a single word.
        9    Treat the image as a single word in a circle.
        10    Treat the image as a single character.
        11    Sparse text. Find as much text as possible in no particular order.
        12    Sparse text with OSD.
        13    Raw line. Treat the image as a single text line,
            bypassing hacks that are Tesseract-specific.
        """
        
        text_recog_result = pytesseract.image_to_data(thresholding_img,
                                                      output_type=Output.DICT,
                                                      config='--oem 1 --psm 7')
        return text_recog_result['text']

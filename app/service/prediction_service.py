# custom path
import asyncio
import cv2
import numpy as np
import drug_manager
from preprocessing import *
from OCR import READER
from drug_enums import Shape

# TODO; has to be Singleton
class PredictionService:
    def __init__(self, img, is_upload=False):
        # init src from bytes
        if is_upload:
            self.image = self.create_cv2_mode(img)
        else:
            self.image = img
        self.shape = Shape.NotFound

    def preprocessing(self):
        """
            <pipeline>
            1. convert gray
            2. crop object area
            3. crop by shape
        """
        self.pp_image = get_grayscale(self.image)
        self.pp_image = get_object_area(self.pp_image)
        self.crop_by_shape(self.pp_image)

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

    def get_prediction(self):
        color_group = self.get_color_group()
        text_group = self.get_text_group()
        recog_result = color_group & text_group

        result = []
        base_URL = 'https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq='
        for pid in recog_result:
            temp = drug_manager.get_drug(pid)
            temp['webviewURL'] = f"{base_URL}{pid}"
            result.append(temp)
        return result


    def get_color_group(self):
        """use Foreground of image to distribute the group of color

        Args:
            img (numpy.ndarray): result data from Preprocessing.get_foreground
        """
        color_group = []
        for color, values in drug_manager.COLOR_RANGE.items():
            low = values[0]
            high = values[1]
            if is_under_color_range(self.image, low, high):
                color_group.append(color)

        # get pids from reference
        result = set()
        for color in color_group:
            result.update(drug_manager.get_color_pid(color))
        return result

    def crop_by_shape(self, image):
        circles = get_circles(image)
        if circles is not None:
            self.shape = Shape.Circle
            image = get_circle_area(image, circles)

        return image
            

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

    def get_text(self):
        results = READER.readtext(self.pp_image)
        return results

    def get_text_group(self):
        """get option from user and return value by its option

        Args:
            img (UploadedFile): the image data which has uploaded from client
            opt (int): the option will take whether to change the origin data to what
        """
        def clean_text(text):
            return "".join([c if ord(c) < 128 else "" for c in text]).strip()

        def remove_exceptions(text):
            result = ''
            for t in text:
                if t == '(': result += 'C'
                elif t == ']': result += 'J'
                else: result += t
            return result

        def get_candidates(text, i, similars, candidates):
            if i == len(text): return
            for similar in similars:
                if text[i] in similar:
                    for s in similar:
                        converted = ''.join(text[:i] + s + text[i + 1:])
                        candidates.add(converted)
                        get_candidates(converted, i + 1, similars, candidates)
                get_candidates(text, i + 1, similars, candidates)

        results = self.get_text()

        text_recog_result = ''
        for bbox, text, prob in results:
            text_recog_result += clean_text(text) + ' '
        text_recog_result = text_recog_result.strip()

        # check in text ref
        temp = remove_exceptions(text_recog_result)

        candidates = set()
        similars = [['1', 'I', 'J'], ['5', 'S'], ['D', '0', 'O', 'Q'],
                    ['4', 'A'], ['2', '-'], ['Y', 'V']]

        get_candidates(temp, 0, similars, candidates)
        pids = set()
        for candidate in candidates:
            pid_set = drug_manager.get_text_pid(candidate)
            if pid_set is not None:
                pids.update(pid_set)

        return pids

# custom path
import asyncio
import cv2
from service.load import Reference
from service.preprocessing import Preprocessing

# use EasyOCR
import easyocr


# TODO; has to be Singleton
class PredictionService:
    def __init__(self):
        """init from different classes
        - Preprocessing
        - Reference
        """
        self.ref = Reference()
        self.preprocess = Preprocessing()

    async def get_color_group(self, img):
        """use Foreground of image to distribute the group of color

        Args:
            img (numpy.ndarray): result data from Preprocessing.get_foreground
        """
        redLow = (0, 60, 80)
        redHigh = (45, 255, 255)
        greenLow = (45, 15, 10)
        greenHigh = (80, 255, 255)
        blueLow = (90, 60, 70)
        blueHigh = (115, 255, 255)
        blackLow = (0, 0, 0)
        blackHigh = (180, 255, 40)
        whiteLow = (0, 0, 220)
        whiteHigh = (180, 40, 255)

        pp = self.preprocess
        src = pp.create_cv2_mode(img)

        # 색상
        color_arr = []
        pp.get_color(src, redLow, redHigh, "Red", color_arr)
        pp.get_color(src, greenLow, greenHigh, "Green", color_arr)
        pp.get_color(src, blueLow, blueHigh, "Blue", color_arr)
        pp.get_color(src, blackLow, blackHigh, "Black", color_arr)
        pp.get_color(src, whiteLow, whiteHigh, "White", color_arr)

        # get pids from reference
        result = set()
        for key in color_arr:
            result.update(self.ref.color[key])
        return result

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

    async def get_text(self, img):
        """get option from user and return value by its option

        Args:
            img (UploadedFile): the image data which has uploaded from client
            opt (int): the option will take whether to change the origin data to what
        """
        pp = self.preprocess
        ref = self.ref
        # get img converted to cv2 mode
        converted_img = pp.create_cv2_mode(img)
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(converted_img)

        def clean_text(text):
            return "".join([c if ord(c) < 128 else "" for c in text]).strip()

        text_recog_result = ''
        for bbox, text, prob in results:
            text_recog_result += clean_text(text) + ' '
        text_recog_result = text_recog_result.strip()

        def remove_exceptions(text):
            result = ''
            for t in text:
                if t == '(': result += 'C'
                elif t == ']': result += 'J'
                else: result += t
            return result

        # check in text ref
        text_set = set()
        temp = remove_exceptions(text_recog_result)

        candidates = set()
        similars = [['1', 'I', 'J'], ['5', 'S'], ['D', '0', 'O', 'Q'],
                    ['4', 'A'], ['2', '-']]

        def get_candidates(text, i, similars, candidates):
            if i == len(text): return
            for similar in similars:
                if text[i] in similar:
                    for s in similar:
                        converted = ''.join(text[:i] + s + text[i + 1:])
                        candidates.add(converted)
                        get_candidates(converted, i + 1, similars, candidates)
                get_candidates(text, i + 1, similars, candidates)

        get_candidates(temp, 0, similars, candidates)
        
        for candidate in candidates:
            if candidate in ref.text:
                text_set = text_set.union(ref.text[candidate])

        return set(text_set)

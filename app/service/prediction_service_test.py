from prediction_service import PredictionService
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = f'../test/images/image1.jpeg'
image = cv2.imread(path)
prediction_service = PredictionService(image)
prediction_service.preprocessing()
result = prediction_service.get_prediction()
print(result)
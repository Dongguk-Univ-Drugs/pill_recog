import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile
# for concurrency
import asyncio
from time import time
# custom service
from service.prediction_service import PredictionService
from service.drug_manager import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "/static/image")
SERVER_IMAGE_DIR = os.path.join('http:localhost:8000', "/static/image")

# run app
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def health():
    return 'ok'

# file upload
@app.post("/file/")
async def upload_img(file: UploadFile = File(...)):
    # convert `UploadFile` to `numpy.ndarray`
    input_byte_img = await file.read()
    start = time()
    # init Prediction class
    ps = PredictionService(input_byte_img, True)
    result = ps.get_prediction()
    end = time()
    # make result
    return {
        'result': result,
        'time': f'{end - start}s'
    }


# @app.get("/test_darknet")
# def test_darknet():
#     results = darknet_images.test()
#     return results

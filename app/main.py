import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile
# for concurrency
import asyncio
from time import time
# custom service
from service.prediction_service import PredictionService

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "/static/image")
SERVER_IMAGE_DIR = os.path.join('http:localhost:8000', "/static/image")

# init Prediction class
ps = PredictionService()
# run app
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# file upload
@app.post("/file/")
async def upload_img(file: UploadFile = File(...)):
    # convert `UploadFile` to `numpy.ndarray`
    input_byte_img = await file.read()
    start = time()
    text_task = asyncio.create_task(ps.get_text(input_byte_img))
    color_task = asyncio.create_task(ps.get_color_group(input_byte_img))
    text = await text_task
    color = await color_task
    recog_result = text & color
    end = time()
    # make result
    result = []
    base_URL = 'https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq='
    for code in recog_result:
        temp = ps.ref.total[code]
        temp['webviewURL'] = base_URL + code
        result.append(temp)

    return {
        'result': result,
        'time': f'{end - start}s'
    }


# @app.get("/test_darknet")
# def test_darknet():
#     results = darknet_images.test()
#     return results

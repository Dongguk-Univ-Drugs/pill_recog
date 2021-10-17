import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile

from app.service.prediction_service import PredictionService
# from darknet import darknet_images

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "/static/image")
SERVER_IAMGE_DIR = os.path.join('http:localhost:8000', "/static/image")

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
    return {"filename": file.filename}


# @app.get("/test_darknet")
# def test_darknet():
#     results = darknet_images.test()
#     return results

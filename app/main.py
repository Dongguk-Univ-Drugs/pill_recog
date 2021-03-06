import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from darknet import darknet_images

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "/static/image")
SERVER_IAMGE_DIR = os.path.join('http:localhost:8000', "/static/image")
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/test_darknet")
def test_darknet():
    results = darknet_images.test()
    return results


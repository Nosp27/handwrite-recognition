import base64
import time
import abc
from io import BytesIO

import pytesseract
from PIL import Image


class BaseModel(abc.ABC):
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def predict(self, data, lang) -> str:
        pass


class TestModel(BaseModel):
    def __init__(self, *, delay=5):
        super().__init__(delay=delay)
        self.delay = delay

    def predict(self, data, lang) -> str:
        time.sleep(self.delay)
        return "Some recognized text"


class TesseractModel(BaseModel):
    def predict(self, data, lang) -> str:
        img = Image.open(BytesIO(base64.decodebytes(data.split(",", 2)[-1].encode())))
        result = pytesseract.image_to_string(img, lang=lang)
        return result 

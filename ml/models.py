import time
import abc


class BaseModel(abc.ABC):
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def predict(self, data) -> str:
        pass


class TestModel(BaseModel):
    def __init__(self, *, delay=5):
        super().__init__(delay=delay)
        self.delay = delay

    def predict(self, data) -> str:
        time.sleep(self.delay)
        return "Some recognized text"

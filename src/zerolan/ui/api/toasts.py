import uuid
from typing import Literal

import requests

from common.decorators import multithread
from web.entities import ToastEntity, ProgressToastEntity


class Toast:

    def __init__(self, message: str,
                 level: Literal["info", "warn", "error"] = "info",
                 duration: int = 5):
        self.host = "http://127.0.0.1:5000"
        self.id = str(uuid.uuid4())
        self.message = message
        self.level = level
        self.duration = duration

    @multithread
    def show_toast(self):
        json = ToastEntity(id=self.id,
                           message=self.message,
                           level=self.level,
                           duration=self.duration).to_dict()  # type: ignore
        requests.post(f"{self.host}/toast", json=json)

    def set_message(self, message: str = None, cur_value: int = None):
        if message is not None:
            requests.put(f"{self.host}/toast/{self.id}", json={"message": message})
        if cur_value is not None:
            requests.put(f"{self.host}/toast/{self.id}", json={"value": cur_value})

    def close_toast(self):
        requests.delete(f"{self.host}/toast/{self.id}")

    def __enter__(self):
        self.show_toast()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_toast()


class ProgressToast(Toast):
    def __init__(self, message: str,
                 level: Literal["info", "warn", "error"] = "info",
                 duration: int = 5,
                 busy: bool = True,
                 max_value: int = 100,
                 cur_value: int = 0):
        super().__init__(message=message, level=level, duration=duration)
        self.busy = busy
        self.max_value = max_value
        self.cur_value = cur_value

    @multithread
    def show_toast(self):
        json = ProgressToastEntity(id=self.id,
                                   message=self.message,
                                   level=self.level,
                                   duration=self.duration).to_dict()  # type: ignore
        requests.post(f"{self.host}/toast/progress", json=json)

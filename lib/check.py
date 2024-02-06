import functools
from functools import wraps
from typing import Any, Dict, List

import config.config as cf

_State: List[Dict[str, Any]] = []


class Manager:
    @staticmethod
    def _init():
        global _State

    @staticmethod
    def set_module(config, func):
        _State.append({"c": config, "m": func, "t": 0})

    @staticmethod
    def add_time(id):
        _State[id]["t"] += 1

    @staticmethod
    def clear_time(id):
        _State[id]["t"] = 0

    @staticmethod
    def equal_time(id):
        if _State[id]["t"] >= _State[id]["c"]["task_time"]:
            return True
        return False

    @staticmethod
    def set_status(pid: int, status: int):
        _State[pid]["c"]["status"] = status

    @staticmethod
    def get_func(id):
        return _State[id]["m"]

    @staticmethod
    def get_module():
        return _State


class Check:
    def __init__(self):
        self.check = True
        self.config = []
        self.ok = []

    def get_item(self, id):
        for k, item in enumerate(self.config):
            if item["id"] == id:
                return k, item

    def run(self, name, task_time=None):
        def decorate(func):
            # decorate.__func = func
            # print(func.__code__)

            config = {}
            config["name"] = name
            if task_time is None:
                config["task_time"] = cf.default_task_time
            else:
                config["task_time"] = task_time
            config["status"] = 0
            # print(func.__name__)
            Manager.set_module(config, func)

            # print(str(func)+"测试")
            # index, item = self.get_item(id)
            # self.config[index]['status'] = 0
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # print("测一下试")
                # try:
                #     rs = func(*args, **kwargs)
                # except:
                #     print(func.__name__ + "任务执行出错")
                #     rs = None
                #
                # if not rs:
                #     index, item = self.get_item(id)
                #     self.config[index]['status'] = 1
                return

            return wrapper

        return decorate

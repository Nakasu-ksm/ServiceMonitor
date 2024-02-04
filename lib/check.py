import functools
from functools import wraps
import config.config as cf

class Manager():
    @staticmethod
    def _init():
        global _State
        _State = []
    @staticmethod
    def set_module(config, module):
        _State.append({"c": config, "m": module,'t':0})

    @staticmethod
    def add_time(id):
        _State[id]["t"] += 1

    @staticmethod
    def clear_time(id):
        _State[id]['t'] = 0

    @staticmethod
    def equal_time(id):
        if _State[id]['t'] >= _State[id]['c']['task_time']:
            return True
        return False

    @staticmethod
    def get_func(id):
        return _State[id]['m']


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
            if item['id'] == id:
                return k, item

    def run(self, name,task_time=None):
        def decorate(func):
            dic = dict()
            dic['name'] = name
            if not task_time:
                dic['task_time'] = cf.default_task_time
            else:
                dic['task_time'] = task_time
            Manager.set_module(dic, func)
            # index, item = self.get_item(id)
            # self.config[index]['status'] = 0
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print("测试")
                try:
                    rs = func(*args, **kwargs)
                except:
                    print(func.__name__+"任务执行出错")
                    rs = None

                if not rs:
                    index, item = self.get_item(id)
                    self.config[index]['status'] = 1
                return

            return wrapper

        return decorate

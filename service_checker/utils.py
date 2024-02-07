# -*- coding: utf-8 -*-
import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:  # 加锁
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

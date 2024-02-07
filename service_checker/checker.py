# -*- coding: utf-8 -*-
"""
Copyright (c) 2008-2024 Nakasu-ksm sif2@livelive.animed.jp and synodriver <diguohuangjiajinweijun@gmail.com>
"""
import asyncio
import functools
import traceback
from contextvars import copy_context
from functools import partial, wraps
from typing import Any, Awaitable, Callable, Coroutine, List, Union, Dict, Optional
import inspect
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from service_checker.utils import SingletonType


def run_sync(call: Callable) -> Callable:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        context = copy_context()
        result = await loop.run_in_executor(None, partial(context.run, pfunc))
        return result

    return _wrapper


Runner_T = Callable[[], Union[Any, Awaitable[Any]]]


class Checker(metaclass=SingletonType):
    def __init__(self):
        self.funcs: List[Runner_T] = []
        self.scheduler = AsyncIOScheduler()
        self.data: List[Dict[...]] = []

    async def _template(self, func, index):
        print(inspect.iscoroutinefunction(func))
        try:
            if inspect.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
        except Exception as e:
            raise RuntimeError("Plugin_"+func.__module__+" excute wrong")
        if result:
            self.data[index]['status'] = 0
        else:
            self.data[index]['status'] = 1



    def register(self, task_time: float = 5.0, service_name: str = Optional[str]) -> Callable[[Runner_T], Runner_T]:
        def inner(func: Runner_T) -> Runner_T:
            print(inspect.signature(func))
            self.data.append({'status': 0, "service_name": service_name})
            index = len(self.data)-1
            self.funcs.append(func)
            if not asyncio.iscoroutinefunction(func):
                func_ = run_sync(func)
            else:
                func_ = func
            self.scheduler.add_job(self._template, "interval", seconds=task_time, args=[func_, index])
            return func

        return inner

    def unregister(self, func: Runner_T) -> None:
        self.funcs.remove(func)

    def run(self):
        self.scheduler.start()

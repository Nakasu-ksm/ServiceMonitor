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

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from service_checker.SingletonType import SingletonType
from service_checker.utils.helper import Helper


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
        self.index : int = 0
        self.funcs: List[Runner_T] = []
        self.scheduler = AsyncIOScheduler()
        self.data: List[Dict[...]] = []

    def _get_data(self):
        return self.data

    async def _core(self, func, optional:Dict):
        is_success = False
        try:
            # 存在url的方案
            if "url" in optional:
                res = httpx.request(optional["url_method"], optional['url'])
                if res.status_code == 200:
                    is_success = True
            else:
                if inspect.iscoroutinefunction(func):
                    result = await func()
                else:
                    result = func()

                if result:
                    is_success = True
        except Exception as e:
            raise e


        if is_success:
            self.data[optional['index']]['status'] = 0
        else:
            self.data[optional['index']]['status'] = 1

    def register(self, task_time: float = 5.0, service_name: str = Optional[str], simple_url:str = None, url_code:List[int]=[200], url_method:str="GET") -> Callable[[Runner_T], Runner_T]:
        def inner(func: Runner_T) -> Runner_T:

            binding_data = dict()
            # 载入类型
            inf = inspect.signature(func).parameters
            for name, parm in inf.items():
                if parm.annotation == Helper:
                    binding_data[name] = Helper()

            func = partial(func, **binding_data)



            # print(inspect.signature(func))
            self.data.append({"id": self.index, 'status': 0, "service_name": service_name})
            self.index += 1
            index = len(self.data) - 1
            self.funcs.append(func)
            if not asyncio.iscoroutinefunction(func):
                func_ = run_sync(func)
            else:
                func_ = func
            optional = dict()
            optional['url_method'] = url_method
            optional['index'] = index

            if not isinstance(url_code, List):
                raise SystemError("only accept list")
            optional['url_code'] = url_code
            if simple_url is not None:
                optional['url'] = simple_url
            self.scheduler.add_job(self._core, "interval", seconds=task_time, args=[func_, optional])
            return func

        return inner

    def unregister(self, func: Runner_T) -> None:
        self.funcs.remove(func)

    def run(self):
        self.scheduler.start()

# -*- coding: utf-8 -*-
"""
Copyright (c) 2008-2024 synodriver <diguohuangjiajinweijun@gmail.com>
"""
import asyncio
from contextvars import copy_context
from functools import partial, wraps
from typing import Any, Awaitable, Callable, Coroutine, List, ParamSpec, TypeVar, Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from service_checker.utils import SingletonType

P = ParamSpec("P")
R = TypeVar("R")


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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

    def register(self, task_time: float = 5.0) -> Callable[[Runner_T], Runner_T]:
        def inner(func: Runner_T) -> Runner_T:
            self.funcs.append(func)
            if not asyncio.iscoroutinefunction(func):
                func_ = run_sync(func)
            else:
                func_ = func
            self.scheduler.add_job(func_, "interval", seconds=task_time)
            return func

        return inner

    def unregister(self, func: Runner_T) -> None:
        self.funcs.remove(func)

    def run(self):
        self.scheduler.start()

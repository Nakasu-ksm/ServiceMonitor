import time
from threading import Thread

from lib.check import Manager


class Task(Thread):
    def __init__(self):
        # Manager.get_module()[0]['m']()
        self.run()

    def _templete(self, func, pid):
        try:
            result = func()
            if result:
                return Manager.set_status(pid, 0)
            return Manager.set_status(pid, 1)
        except Exception:
            print(func.__module__ + ":" + func.__name__ + ":方法执行异常")

    def _task(self):
        print("任务模块启动成功!")
        while True:
            for pid in range(len(Manager.get_module())):
                Manager.add_time(pid)
                if Manager.equal_time(pid):
                    Thread(target=self._templete(Manager.get_func(pid), pid)).start()
                    Manager.clear_time(pid)
            time.sleep(1)

    def run(self):
        self._task()

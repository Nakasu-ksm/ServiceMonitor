from threading import Thread
import time
from lib.check import Manager


class Task(Thread):
    def __init__(self):
        self.run()
    def _task(self):
        print("任务模块启动成功!")
        while True:
            for pid in range(len(Manager.get_module())):
                Manager.add_time(pid)
                if Manager.equal_time(pid):
                    Thread(target=Manager.get_func(pid)).start()
                    Manager.clear_time(pid)
            time.sleep(1)

    def run(self):
        thread = Thread(target=self._task)
        thread.start()



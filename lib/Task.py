from threading import Thread
import time
from lib.check import Manager

class Task(Thread):
    def __init__(self):

        Manager.get_module()[0]['m']()
        self.run()
    def _templete(self, func,pid):
        result = func()
        if result:
            return Manager.set_status(pid, 0)
        return Manager.set_status(pid,1)


    def _task(self):
        print("任务模块启动成功!")
        while True:
            for pid in range(len(Manager.get_module())):
                Manager.add_time(pid)
                if Manager.equal_time(pid):
                    Thread(target=self._templete(Manager.get_func(pid),pid)).start()
                    # Manager.get_func(pid)()
                    # print(Manager.get_func(pid))
                    Manager.clear_time(pid)
            time.sleep(1)

    def run(self):
        thread = Thread(target=self._task)
        thread.start()



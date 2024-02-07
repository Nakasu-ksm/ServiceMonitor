from datetime import datetime

from service_checker import Checker

checker = Checker()
# test = []


@checker.register(task_time=5, service_name="服务器1")
async def _():
    """5s一次"""
    print(f"5s一次 {datetime.now()}")
    return "2"[2]
    return True


@checker.register(task_time=2, service_name="服务器2")
async def _():
    print(f"2s一次 {datetime.now()}")
    return False

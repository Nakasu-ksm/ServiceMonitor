from datetime import datetime
from service_checker import Checker
from service_checker.utils.helper import Helper

checker = Checker()
# test = []

@checker.register(task_time=5, service_name="服务器1")
def _(helper : Helper):
    return helper.get_result("https://cbaisdasadu.com")


# @checker.register(task_time=2, service_name="服务器2")
# async def _():
#     print(f"2s一次 {datetime.now()}")
#     return False


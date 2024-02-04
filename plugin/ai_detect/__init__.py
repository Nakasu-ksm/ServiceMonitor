from lib.check import *

check = Check()
test = []


@check.run(name="测试服务器")
def _():
    return False


@check.run(name="测试方法")
def ces():
    # a = "cc"
    # a['3']
    return True


ces()
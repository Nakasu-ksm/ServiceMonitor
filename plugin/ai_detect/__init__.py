from datetime import datetime

from service_checker import Checker

checker = Checker()
# test = []


@checker.register(5)
async def _():
    """5s一次"""
    print(f"5s一次 {datetime.now()}")
    return False


@checker.register(2)
async def _():
    print(f"2s一次 {datetime.now()}")
    return True

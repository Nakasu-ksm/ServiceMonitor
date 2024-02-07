import httpx
from fastapi import FastAPI

# from lib.Testing import Testing
#
# client = httpx.AsyncClient(timeout=20)
# testing_app = Testing()
import asyncio
from service_checker import Checker, Plugin

app = FastAPI()


def main():
    plugin = Plugin()
    plugin.load_module()
    checker = Checker()
    checker.run()


main()
# if __name__ == "__main__":
#     main()

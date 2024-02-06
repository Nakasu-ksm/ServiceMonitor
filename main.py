import httpx
from fastapi import FastAPI

# from lib.Testing import Testing
#
# app = FastAPI()
# client = httpx.AsyncClient(timeout=20)
# testing_app = Testing()
import asyncio
from service_checker import Checker, Plugin

async def main():
    plugin = Plugin()
    plugin.load_module()

    checker = Checker()
    checker.run()
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
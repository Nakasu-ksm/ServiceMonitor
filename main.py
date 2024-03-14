import httpx
from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve

from service_checker.utils.utils import Core

# from lib.Testing import Testing
#
app = FastAPI()
# client = httpx.AsyncClient(timeout=20)
# testing_app = Testing()
import asyncio
from service_checker import Checker, Plugin


@app.get("/status")
async def _():
    return Core().get_status()


async def main():
    plugin = Plugin()
    plugin.load_module()

    checker = Checker()
    checker.run()
    config = Config.from_mapping({"bind": "0.0.0.0:8000"})
    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
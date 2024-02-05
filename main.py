import httpx
from lib.Testing import Testing
from fastapi import FastAPI
app = FastAPI()
client = httpx.Client(timeout=20)
testing_app = Testing()
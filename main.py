import json

import requests
from flask import Flask
import datetime
import lib.manager as mg
import httpx
from lib.Task import *
from lib.check import *
from lib.plugin import Plugin
from flask_cors import cross_origin
from lib.Testing import Testing
from flask_apscheduler import APScheduler
app = Flask(__name__)
client = httpx.Client(timeout=20)
testing_app = Testing()

@app.get("/serviceStatus")
@cross_origin()
def service():
    global test_urls
    data = {"status":200, "data":[]}
    data['data'] = []
    for item in test_urls:
        service = {}
        service['name'] = item['name']
        service['status'] = item['status']
        if 'default_error' in item:
            service['default_error'] = item['default_error']
        if 'default_ok' in item:
            service['default_ok'] = item['default_ok']
        data['data'].append(service)
    return json.dumps(data)



if __name__ == '__main__':
    app.run(port=8000, debug=False)

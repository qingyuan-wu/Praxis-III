import requests as req
import time
from random import randint
PORT = 4003
URL = f"http://localhost:{PORT}"

data_obj = {"temp": "200", "brightness": "4334"}

i = 0
while True:
    req.post(URL, data={ "type": randint(1,2)})
    i += 1
    print(i, req)
    time.sleep(5)


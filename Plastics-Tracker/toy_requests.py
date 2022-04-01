import requests as req
import time
from random import randint
PORT = 4003
URL = f"http://localhost:{PORT}"
data={ "type": randint(1,2), "request": "newdata" }


i = 0
while True:
    req.post(URL, data=data)
    i += 1
    print(i, req)
    time.sleep(5)


import requests as req
import time
from random import randint
PORT = 4003
URL = f"http://localhost:{PORT}"

i = 0
while True:
    print(i)
    req.post(URL, data={ "type": '1' })
    i += 1
    print(i, req)
    time.sleep(5)
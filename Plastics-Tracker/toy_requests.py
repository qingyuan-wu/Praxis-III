import requests as req
import time
from random import randint
PORT = 4003
URL = f"http://localhost:{PORT}"



i = 0
for x in range(20):
    data={ "type": randint(1,2)}
    req.post(URL, data=data)
    i += 1
    print(i, req)
    time.sleep(2)


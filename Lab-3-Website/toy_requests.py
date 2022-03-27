import requests as req
import time
PORT = 4003
URL = f"http://localhost:{PORT}"

data_obj = {"temp": "200", "brightness": "4334"}

i = 0
while True:
    req.post(URL, data={ "temp": i, "brightness": 100 })
    i += 1
    print(i, req)
    time.sleep(5)


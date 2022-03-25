import requests as req
import time
PORT = 4003
URL = f"http://localhost:{PORT}"

data_obj = {"temp": "300"}

i = 0
while True:
    req.post(URL, data={ "test": i })
    i += 1
    print(i, req)
    time.sleep(5)


import requests as req
PORT = 4003
URL = f"localhost://{PORT}"
data_obj = {"temp": "300"}

req.send(URL, data_obj)
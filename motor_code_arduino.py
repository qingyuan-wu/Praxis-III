'''
Purpose: rotate motor up and down to faciliate physical sorting of plastics
'''

import board
import time
import digitalio
import pwmio

# imports for wifi connections
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

#  ESP32 pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

#  uses the secondary SPI connected through the ESP32
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

# pin mappings (we swtiched from Pico to Arduino Nano)
# (orange) GP16 -> D4, GPIO16
# (black) GND -> GND
# (yellow) GP15 -> D2, GPIO25
# (blue) GP14 -> D3, GPIO15

# for respberry pico: direction pins as digital outputs
# in1 = digitalio.DigitalInOut(board.GP14)
# in2 = digitalio.DigitalInOut(board.GP15)
# in1.direction = digitalio.Direction.OUTPUT
# in2.direction = digitalio.Direction.OUTPUT

# for arduino nano: pins
in1 = digitalio.DigitalInOut(board.D3)
in2 = digitalio.DigitalInOut(board.D2)
in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT

# set up LED as PWM output
ena = pwmio.PWMOut(board.D4, duty_cycle = 0)

# set time limits
start_time = time.time()
time_limit = 20

# set starting (fastest) motor duty cycles
CW_duty = 65000
CCW_duty = 65000
duty_step = 5000
max_int = 65535
up = False # initial configuration is down
# lower box: PET
# upper box: not PET

# NOTE: localhost will not work since arduino is getting the data and has no clue what localhost is!
# URL = "http://localhost:4000/forum"

URL = "http://www.randomnumberapi.com/api/v1.0/random?min=1&max=2&count=1"
print("Fetching plastic type from", URL)

while True:
    r = requests.get(URL)
    plastic_type = r.json()[0]
    r.close()

    # 1 for PET, 2 for not PET
    print(f"Last plast: type {plastic_type}. Slider is currently up = {up}")
    if plastic_type == 1 and up:
        # rotate CW - rotate down
        in1.value, in2.value = (False, True)
        ena.duty_cycle = CW_duty
        print(f"Rotating CW at {100*CW_duty/max_int} duty cycle")
        CW_duty = CW_duty - duty_step
        time.sleep(1.8) # rotate for 1.8 seconds
        ena.duty_cycle = 0
        # state has changed:
        up = not up

    elif plastic_type == 2 and not up:
        # rotate CCW - rotate up
        # rotate counterclockwise
        in1.value, in2.value = (True, False)
        ena.duty_cycle = CCW_duty
        print(f"Rotating CCW at {100*CW_duty/max_int} duty cycle")
        CCW_duty = CCW_duty - duty_step
        time.sleep(1.8) # rotate for 1.8 seconds
        ena.duty_cycle = 0
        # state has changed:
        up = not up

    time.sleep(1)
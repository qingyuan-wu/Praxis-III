'''
ESC204 2022W Widget Lab 3IoT, Part 9
Task: Publish sensor data to Adafruit IO Dashboard using MQTT.
'''
# SPDX-FileCopyrightText: Brent Rubell for Adafruit Industries # SPDX-License-Identifier: MIT
import time
from microcontroller import cpu
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

import analogio

print("start")
# Define callback functions which will be called when certain events happen. # pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO! ")

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))
# pylint: disable=unused-argument

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

def on_led_msg(client, topic, message):
# Method called whenever user/feeds/led has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    if message == "ON":
        led_pin.value = True
    elif message == "OFF":
        led_pin.value = False
    else:
        print("Unexpected message on LED feed.")
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
# Set up SPI pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# Connect RP2040 to the WiFi module's ESP32 chip via SPI, then connect to WiFi
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# Configure the RP2040 Pico LED Pin as an output
led_pin = DigitalInOut(board.LED)
led_pin.switch_to_output()

# Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected!")

ADC_HIGH = 65535

# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, esp)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=secrets["port"],
    username=secrets["aio_username"],
    password=secrets["aio_key"],
)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to Adafruit IO
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe

# Set up a callback for the led feed
io.add_feed_callback("led", on_led_msg)

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

# Subscribe to all messages on the led feed
io.subscribe("led")

prv_refresh_time = 0.0


## PHOTORESISTOR --------------------------------------------------------------------------------------------

light_sensor_pin = board.A0
light_sensor = analogio.AnalogIn(light_sensor_pin)

ADC_REFphoto = light_sensor.reference_voltage



print("ADC reference voltage: {}".format(ADC_REFphoto))
print("ADC high voltage integer value: {}".format(ADC_HIGH))

def adc_to_voltagephoto(adc_value):
    return ADC_REFphoto * (float(adc_value)/float(ADC_HIGH))


## Temp Sensor ----------------------------------------------------------------------------------------------------------

thermistor_pin = board.A1
thermistor = analogio.AnalogIn(thermistor_pin)

# show reference voltage (logic high, 3.3V) and the corresponding analog integer value
ADC_REFthermo = thermistor.reference_voltage
print("ADC reference voltage: {}".format(ADC_REFthermo))
print("ADC high voltage integer value: {}".format(ADC_HIGH))


# convert ADC input value back to voltage
def adc_to_voltagethermo(adc_value):
    return  ADC_REFthermo * (float(adc_value)/float(ADC_HIGH))

## ----------------------------------------------------------
# def post_data(data):
#     import requests as req
#     data = {'temperature':data}

#     resp = req.post("http://localhost/4003/", data)

while True:
    # Poll for incoming messages
    try:
        io.loop()
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        io.reconnect()
        continue

# Send a new temperature reading to IO every 30 seconds
    if (time.monotonic() - prv_refresh_time) > 2:
        # take the cpu's temperature
        cpu_temp = cpu.temperature

        # truncate to two decimal points
        cpu_temp = str(cpu_temp)[:5]
        print("CPU temperature is %s degrees C" % cpu_temp)
        # publish it to io
        print("Publishing %s to temperature feed..." % cpu_temp)
        io.publish("temperature", cpu_temp)

        # also set a new photoresistor reading to IO every 5 seconds
        photoresistance = light_sensor.value
        print("Publishing %s to photoresistance feed..." % photoresistance)
        io.publish("photoresistance", adc_to_voltagephoto(photoresistance))

        adctemp = thermistor.value
        #resistancethermo = 10000 /(1023/(adctemp-1))
        print("Publishing %s to temperature feed..." % adctemp)
        io.publish("temperature", adc_to_voltagethermo(adctemp))
            
        prv_refresh_time = time.monotonic()

    #post_data(cpu_temp)


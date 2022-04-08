'''
ESC204 2022W Widget Lab 2, Part 14
Task: Use PWM to modulate the speed of a DC motor.
'''
import board
import time
import digitalio
import pwmio

# get result of ML classification decision
# import urllib3
import random
states = [2,1,2,1]

# set up direction pins as digital outputs
in1 = digitalio.DigitalInOut(board.GP14)
in2 = digitalio.DigitalInOut(board.GP15)
in1.direction = digitalio.Direction.OUTPUT
in2.direction = digitalio.Direction.OUTPUT

# set up LED as PWM output
ena = pwmio.PWMOut(board.GP16, duty_cycle = 0)

# set time limits
start_time = time.time()
time_limit = 20

# set starting (fastest) motor duty cycles
CW_duty = 65000
CCW_duty = 65000
duty_step = 5000
max_int = 65535
up = False
# lower box: PET
# upper box: not PET
# rotate motor shaft in alternating directions with gradually decreasing speed
for plastic_type in states:
    URL = "http://localhost:4003/type"
    #resp = req.get(URL)
    #print(resp)
    #plastic_type = random.randint(1,2) # 1 for PET, 2 for not PET
    print(f"Type {plastic_type}. Slider is currently up = {up}")
    if plastic_type == 1 and up:
        # rotate CW - rotate down
        in1.value, in2.value = (False, True)
        ena.duty_cycle = CW_duty
        print(f"Rotating CW at {100*CW_duty/max_int} duty cycle")
        CW_duty = CW_duty - duty_step
        time.sleep(1.8) # rotate for 1.5 seconds
        ena.duty_cycle = 0
        up = not up

    elif plastic_type == 2 and not up:
        # rotate CCW - rotate up
        # rotate counterclockwise
        in1.value, in2.value = (True, False)
        ena.duty_cycle = CCW_duty
        print(f"Rotating CCW at {100*CW_duty/max_int} duty cycle")
        CCW_duty = CCW_duty - duty_step
        time.sleep(1.8) # rotate for 1.5 seconds
        ena.duty_cycle = 0
        up = not up

    time.sleep(2)

    # stop if time limit reached
    #if time.time() - start_time > time_limit:
     #   break
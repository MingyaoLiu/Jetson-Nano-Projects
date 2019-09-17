import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    while not GPIO.input(21):
        pass
    print("Closed Circuit")
    while GPIO.input(21):
        pass
    print("Opened Circuit")
    sleep(1)

GPIO.cleanup(21)

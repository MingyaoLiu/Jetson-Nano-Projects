import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
import datetime

while True:
    while not GPIO.input(21):
        pass
    print("Closed Circuit", )
    while GPIO.input(21):
        pass
    now = datetime.datetime.now()
    print("Opened Circuit", now.date)
    sleep(1)

GPIO.cleanup(21)

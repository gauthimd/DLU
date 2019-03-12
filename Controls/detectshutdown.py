import RPi.GPIO as GPIO
import time
from subprocess import call
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
def shutdown():
  call("sudo shutdown -h now", shell=True)
while True:
  try:
    if GPIO.wait_for_edge(21, GPIO.FALLING):
      shutdown()
    else: time.sleep(.001)
  except KeyboardInterrupt:
    GPIO.cleanup()

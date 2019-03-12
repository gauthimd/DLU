from datetime import datetime, timedelta

def delay(msec):
  delay = timedelta(milliseconds=msec)
  now = datetime.now()
  then = now + delay
  while True:
    if now < then:
      now = datetime.now()
      continue
    else: break

def printshit(string):
    print(string)

printshit('hello')
delay(2650)
printshit('goodbye')

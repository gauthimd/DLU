from datetime import datetime, timedelta
delay = timedelta(milliseconds=250)
then = datetime.now() + delay
while True:
  now = datetime.now()
  if now > then:
    print("hello")
    then = now + delay
  else:pass

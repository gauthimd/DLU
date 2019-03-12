from datetime import datetime
import sqlite3
from application.config.base_config import DB_PATH
program = 0
delay = 0.5
bright = 1.0
led1 = 1
led2 = 2
led3 = 3
lights = "{0} {1} {2}".format(led1,led2,led3)
power = 0
mode = 1
shifter = 1
timerset = 0
ontime = datetime.strptime("19:30","%H:%M")
offtime = datetime.strptime("7:00","%H:%M")
now = datetime.now().strftime('%b %d, %Y %H:%M:%S')
status = [program, delay, bright, lights, power, mode, shifter,
          timerset, ontime.strftime("%H:%M"), offtime.strftime("%H:%M"),
          now]
try:
  db = sqlite3.connect(DB_PATH)
  cur = db.cursor()
  cur.execute('''INSERT INTO status(program, delay, bright, lights,
              power, mode, shifter, timerset, ontime, offtime, timestamp
              ) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', status)
  db.commit()
  db.close()
except Exception as e:
  raise e

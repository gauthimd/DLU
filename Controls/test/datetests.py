#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlite3, time
hello = datetime.now()
timestamp  = hello.strftime('%b %d, %Y %H:%M:%S')
print(timestamp)
ontime = "18:30"
offtime = "6:30"
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''INSERT INTO status(ontime, offtime, timestamp) 
              VALUES(?,?,?)''', (ontime, offtime, timestamp))
  db.commit()
  db.close
except Exception as e:
  raise e
print('Database updated')
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT timestamp, ontime, offtime FROM status
                 ORDER BY id DESC LIMIT 1''')
  rows = cur.fetchone()
  newontime = datetime.strptime(rows[1],'%H:%M')
  newofftime = datetime.strptime(rows[2],'%H:%M')
  ftime = datetime.strptime(rows[0],'%b %d, %Y %H:%M:%S')
  db.close()
  print(ftime.hour,":",ftime.minute)
  print(newontime.hour,":",newontime.minute)
  print(newofftime.hour,":",newofftime.minute)
except Exception as e:
  raise e

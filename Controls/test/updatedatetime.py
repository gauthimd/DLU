#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
now = datetime.now()
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''INSERT INTO status(timestamp)
                   VALUES(?)''', (now,))
  db.commit()
  db.close()
except: print("It's fuckered")

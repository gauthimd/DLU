#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT id, name, hexcode FROM colors ORDER BY id DESC LIMIT 1''')
  stat = cur.fetchone()
  x = stat[0]
  y = stat[1]
  z = stat[2]
  print(x,y,z)
except Exception as e: raise e

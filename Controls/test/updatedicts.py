#!/usr/bin/python
# -*- coding: utf-8 -*-
from colors import Color
import sqlite3
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT id, hexcode FROM colors''')
  rows = cur.fetchall()
  c = {}
  for row in rows:
    c[row[0]] = Color(row[1])
  print("c = ",c) 
  d = {y:x for x,y in c.items()}
  print("d = ",d)
except Exception as e:# print("Nope")
  raise e

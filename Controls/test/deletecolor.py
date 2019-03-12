#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
name = "brass"
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT id FROM colors WHERE name=?''',(name,))
  row = cur.fetchone()
  if row[0] > 8:
    cur.execute('''DELETE FROM colors WHERE name=?''',(name,))
    db.commit()
  db.close()
except: pass

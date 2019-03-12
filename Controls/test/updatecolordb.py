#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
hexcode = '#f1c9a0'
name = "brass"
db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
cur = db.cursor()
cur.execute('''INSERT INTO colors(name, hexcode)
                 VALUES(?,?)''', (name, hexcode))
db.commit()
db.close()

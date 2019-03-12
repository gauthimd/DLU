#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3

command = input("Enter command: ")
arg1 = input("\nEnter arg1: ")
arg2 = input("\nEnter arg2: ")
arg3 = input("\nEnter arg3: ")

try:
  db = sqlite3.connect('/home/pi/DockLights/db/data.db')
  cur = db.cursor()
  cur.execute('''INSERT INTO commands(command,arg1,arg2,arg3) 
              VALUES(?,?,?,?)''',(command,arg1,arg2,arg3))
  db.commit()
  db.close()
except Exception as e:
  raise e

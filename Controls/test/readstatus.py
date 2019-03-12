#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
try:
  db = sqlite3.connect('/home/pi/DockLights/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT program,delay,bright,lights,power,mode,shifter,
                 sync, timerset, ontime, offtime, timestamp
                 FROM status ORDER BY id DESC LIMIT 1''')
  stat = cur.fetchone()
  x = stat[3]
  y = x.split()
  z = []
  for i in y:
    z.append(i)
  status = {"program":int(stat[0]),"delay":round(float(stat[1]),1),
            "bright":round(float(stat[2]),2),"lights":z, 
            "power":int(stat[4]),"mode":int(stat[5]),
            "shifter":int(stat[6]),"sync":int(stat[7]),"timerset":int(stat[8]),
            "ontime":stat[9],"offtime":stat[10],"timestamp":stat[11]}
  print("*********************************************************************")
  print(status)
  print("*********************************************************************")
except Exception as e: raise e

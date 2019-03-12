#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3, queue, threading, time

def checkcodes(q):
  th = threading.currentThread()
  while getattr(th, "do_run", True):
    try:
      db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
      cur = db.cursor()
      cur.execute('''SELECT command,arg1,arg2,arg3 FROM commands''')
      data = cur.fetchone()
      if data[0] == "colors":
        print('yes')
        print(data[1])
        u = [int(data[1]),int(data[2]),int(data[3])]
        print(u)
        x = {str(data[0]):u}
        print(x)
      else:
        x = {str(data[0]):str(data[1])}
      q.put(x)
      cur.execute('''DELETE FROM commands WHERE command=?''',(data[0],))
      db.commit()
      db.close()
      time.sleep(.1)
    except: pass

def run():
  q = queue.Queue()
  t1 = threading.Thread(target=checkcodes, args=(q,))
  t1.daemon = True
  t1.start()
  while True:
    try:
      y = q.get()
      if y.get("power"):
        if int(y["power"]) == 1: print("jackpot")
      if y.get("colors"):
        x = y["colors"]
        i=0
        for z in x:
          print(x[i])
          i+=1
    except KeyboardInterrupt:
      break
  try:
    t1.do_run = False
    t1.join()
  except: pass
run()

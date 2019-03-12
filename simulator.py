#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, random, threading, queue, json, os, sys, sqlite3
from Controls.colors import Color
from Controls.LEDsimulator import LED
from Controls.sqlhelper import sqlhelper
from datetime import datetime, timedelta
from application.config.base_config import DB_PATH

sqlhelper = sqlhelper()

class System():

  def __init__(self):
      try:
        status = sqlhelper.readstatus()
        self.program = status["program"]
        self.delay = status["delay"]
        self.bright = status["bright"]
        self.power = status["power"]
        self.mode = status["mode"]
        self.shifter = status["shifter"]
        self.sync = status["sync"]
        self.timerset = status["timerset"]
        self.ontime = datetime.strptime(status["ontime"],"%H:%M")
        self.offtime = datetime.strptime(status["offtime"],"%H:%M")
      except:
        self.program = 0
        self.delay = 0.5
        self.bright = 1.0
        self.power = 0
        self.mode = 1
        self.shifter = 0
        self.sync = 1
        self.timerset = 0
        self.ontime = datetime.strptime("18:30","%H:%M")
        self.offtime = datetime.strptime("6:30","%H:%M")
      led1 = LED(0,1,2) #instantiate 3 LED objects for this 3 bulb system
      led2 = LED(3,4,5) #LED(R,G,B) = PWM board pin numbers
      led3 = LED(6,7,8)
      global t # list used to cycle thru each bulb
      t = [led1, led2, led3] # one LED object per rgb bulb
      global c #dicts used for holding color object references
      c = sqlhelper.updatedicts() # returns dictionary c = {pk:color object}
      global m # list of mode methods
      global m2 # list of colors used in certain methods (key in m2 is fk to m)
      m,m2 = self.updatemodes()
      sqlhelper.getmodenames()

  def updatemodes(self):
      modes = sqlhelper.getmodes()
      modedict = {}
      schemedict = {}
      for x in modes:
          z = getattr(self,x[2])
          if x[3] is not None:
            schem = x[3].split(',')
            schem = list(map(int,schem))
          else:
            schem = None
          modedict[x[0]] = z
          if schem != None:
            schemedict[x[0]] = schem
          else: pass
      return modedict, schemedict

  def writestatus(self):
      now = datetime.now().strftime('%b %d, %Y %H:%M:%S')
      lights = "{0} {1} {2}".format(t[0].color, t[1].color, t[2].color)
      update = (self.program, self.delay, self.bright, lights,
                self.power, self.mode, self.shifter, self.sync, self.timerset,
                self.ontime.strftime("%H:%M"), self.offtime.strftime("%H:%M"), now)
      sqlhelper.writeupdate(update)

  def turnon(self, color): # color must be a color primary key or string hexcode "#AA33FF"
      c = sqlhelper.updatedicts()
      try: 
          ncolor = c[color] # try and find color object in dict c from primary key
      except: 
          ncolor = Color(color) # if that fails the color object is generated from hexcode
      for x in t: 
          x.redpwm = int(ncolor.redpwm*self.bright)
          x.greenpwm = int(ncolor.greenpwm*self.bright)
          x.bluepwm = int(ncolor.bluepwm*self.bright)
          x.color = color

  def turnon3separate(self, colors): # colors must be list of color primary keys or string hexcodes "#AA33FF"
      c = sqlhelper.updatedicts()
      ncolors = []
      try: # try and find color objects in dict c from primary keys
          for color in colors:
              ncolors.append(c[color])
      except:  # if that fails the color objects are generated from hexcodes
          for color in colors:
              ncolors.append(Color(color))
      y = 0
      for x in t:
          x.redpwm = int(ncolors[y].redpwm*self.bright)
          x.greenpwm = int(ncolors[y].greenpwm*self.bright)
          x.bluepwm = int(ncolors[y].bluepwm*self.bright)
          x.color = colors[y]
          y += 1
          if y >= len(colors): y = 0
          
  def turnoff(self):
      for x in t:
          x.redpwm = 0
          x.greenpwm = 0
          x.bluepwm = 0

  def fadeoff(self):
    u = []
    for x in t:
      limit = max(x.redpwm, x.greenpwm, x.bluepwm)
      u.append(limit)
    limit = max(u)
    for x in t:
      x.redpwm = 0
      x.greenpwm = 0
      x.bluepwm = 0

  def shift3separate(self, colors): # colors must be list of color primary keys or string hexcodes "#AA33FF"
    c = sqlhelper.updatedicts()
    ncolors = []
    try: # try and find color objects in dict c from primary keys
      for color in colors:
        ncolors.append(c[int(color)])
    except:  # if that fails the color objects are generated from hexcodes
      for color in colors:
        ncolors.append(Color(color))
    u = []
    y = 0
    for x in t:
      maxdiff = max(abs(x.redpwm - ncolors[y].redpwm*self.bright), abs(x.greenpwm - ncolors[y].greenpwm*self.bright), abs(x.bluepwm - ncolors[y].bluepwm*self.bright))
      x.reddiff = abs(x.redpwm - ncolors[y].redpwm*self.bright)
      x.greendiff = abs(x.greenpwm - ncolors[y].greenpwm*self.bright)
      x.bluediff = abs(x.bluepwm - ncolors[y].bluepwm*self.bright)
      u.append(maxdiff)
      y += 1
      if y >= len(t): y = 0
    maxdiff = max(u)
    y = 0
    for x in t:
      x.redpwm = int(ncolors[y].redpwm*self.bright)
      x.greenpwm = int(ncolors[y].greenpwm*self.bright)
      x.bluepwm = int(ncolors[y].bluepwm*self.bright)
      x.color = colors[y]
      y += 1
      if y >= len(t): y = 0

  def shift(self, color): # color must be a color primary key or string hexcode "#AA33FF"
    c = sqlhelper.updatedicts()
    try: 
        ncolor = c[color] # try and find color object in dict c from primary key
    except: 
        ncolor = Color(color) # if that fails the color object is generated from hexcode
    u = []
    for x in t:
      maxdiff = max(abs(x.redpwm - ncolor.redpwm*self.bright), abs(x.greenpwm - ncolor.greenpwm*self.bright), abs(x.bluepwm - ncolor.bluepwm*self.bright))
      x.reddiff = abs(x.redpwm - ncolor.redpwm*self.bright)
      x.greendiff = abs(x.greenpwm - ncolor.greenpwm*self.bright)
      x.bluediff = abs(x.bluepwm - ncolor.bluepwm*self.bright)
      u.append(maxdiff)
    maxdiff = max(u)
    for x in t:
      x.redpwm = int(ncolor.redpwm*self.bright)
      x.greenpwm = int(ncolor.greenpwm*self.bright)
      x.bluepwm = int(ncolor.bluepwm*self.bright)
      x.color = color

  def valentines(self):
    time.sleep(.001)
    ldelay = 1.25
    sdelay = .15
    n = 1
    th = threading.currentThread()
    initim = time.time()
    then = initim + ldelay
    self.turnoff()
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        if n % 2 != 0:
          n += 1
          if n > 4:
            n = 1
            then = now + ldelay
          else:
            then = now + sdelay
        else:
          then = now + sdelay
          n += 1
      else: time.sleep(.001)
    self.turnoff()

  def holidays(self, colors): #colors is list of color primary keys
    th = threading.currentThread()
    x = 0
    y = 1
    if y >= len(colors): y = 0
    z = 2
    if z >= len(colors): z = 0
    initim = time.time()
    delay = 2.78*self.delay+0.22 #puts delay between .5 and 3 seconds
    then = initim
    self.turnoff()
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
          if self.shifter == 0: 
            if self.sync == 0: 
              self.turnon3separate([colors[x],colors[y],colors[z]])
            else: 
              self.turnon(colors[x]) 
          else: 
            if self.sync == 0:
              self.shift3separate([colors[x],colors[y],colors[z]])
            else:
              self.shift(colors[x])
          x += 1
          if x >= len(colors): x = 0
          y += 1
          if y >= len(colors): y = 0
          z += 1
          if z >= len(colors): z = 0
          then = now + delay
      else: time.sleep(.001)
    self.turnoff()

  def randomsync(self):
    th = threading.currentThread()
    delay = 2.78*self.delay + 0.22 #puts delay between .5 and 3 seconds
    then = time.time()
    self.turnoff()
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        y = random.randint(1,len(c))
        if self.shifter == 0: self.turnon(y)
        else: self.shift(y)
        then = now + delay
      else:
        time.sleep(.001)
    self.turnoff()

  def randomcolorasync(self):
    th = threading.currentThread()
    delay = 2.78*self.delay + 0.22 #puts delay between .5 and 3 seconds
    then = time.time()
    self.turnoff()
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        x = self.randcolor()
        y = self.randcolor()
        z = self.randcolor()
        if self.shifter == 0: self.turnon3separate([x,y,z])
        else: self.shift3separate([x,y,z])
        then = now + delay
      else:
        time.sleep(.001)
    self.turnoff()

  def randomasync(self):
    th = threading.currentThread()
    delay = 2.78*self.delay + 0.22 #puts delay between .5 and 3 seconds
    then = time.time()
    self.turnoff()
    while getattr(th, "do_run", True):
      now = time.time()
      if now > then:
        x = random.randint(1,len(c))
        y = random.randint(1,len(c))
        z = random.randint(1,len(c))
        if self.shifter == 0: self.turnon3separate([x,y,z])
        else: self.shift3separate([x,y,z])
        then = now + delay
      else:
        time.sleep(.001)
    self.turnoff()

  def randcolor(self):
    a = '0x{:02x}'.format(random.randint(0,255)).replace('0x','#')
    b = '0x{:02x}'.format(random.randint(0,255)).replace('0x','')
    c = '0x{:02x}'.format(random.randint(0,255)).replace('0x','')
    x = a+b+c
    return x

  def checkcodes(self, q):
    th = threading.currentThread()
    delay = timedelta(milliseconds=1)
    then = datetime.now() + delay
    while getattr(th, "do_run", True):
      now = datetime.now()
      if now > then:
        then = now + delay
        try:
          db = sqlite3.connect(DB_PATH)
          cur = db.cursor() 
          cur.execute('''SELECT command,arg1,arg2,arg3 FROM commands''')
          data = cur.fetchone()
          if data[0] == "colors":
            u = [int(data[1]),int(data[2]),int(data[3])]
            x = {data[0]:u} #sends "colors" args as list of ints for run() engine
          elif data[0] == "save":
            u = [data[1],data[2]]
            x = {data[0]:u} #sends "save" args as list of str ["name","hexcode"]
          elif data[0] == "addmode":
            u = [data[1],data[2]]
            x = {data[0]:u} #sends "addmode" args as list of str ["name","1,2,3"]
          elif data[0] == "ontime":
            self.ontime = datetime.strptime(data[1],"%H:%M")
            self.writestatus()
            x = None
            print("Ontime updated")
          elif data[0] == "offtime":
            self.offtime = datetime.strptime(data[1],"%H:%M")
            self.writestatus()
            x = None
            print("Offtime updated")
          elif data[0] == "timerset":
            u = int(data[1])
            self.timerset = u
            self.writestatus()
            x = None
            print("Timerset updated")
          else: x = {str(data[0]):str(data[1])}
          if x != None:
            q.put(x)
          cur.execute('''DELETE FROM commands WHERE command=?''',(data[0],))
          db.commit()
          db.close()
        except: self.timerengine(now) 

  def enginestatuscheck(self):
      status = sqlhelper.readstatus()
      if status["power"] == 0: 
        self.writestatus()
        t2 = None
      elif status["program"] == 0:
        stat = status["lights"]
        z = [stat[0],stat[1],stat[2]]
        self.shift3separate(z)
        self.power = 1
        self.writestatus()
        t2 = None
      elif status["program"] == 1:
        self.mode = status["mode"]
        m,m2 = self.updatemodes()
        if self.mode in m2:
          t2 = threading.Thread(target=m[self.mode],args=(m2[self.mode],))
        else: t2 = threading.Thread(target=m[self.mode])
        t2.daemon = True
        t2.start()
        self.power = 1
        self.writestatus()
      return t2
 
  def timerengine(self,now): # now must be datetime object
      if self.timerset == 1:
        if self.ontime.hour == now.hour and self.ontime.minute == now.minute: 
          if self.power == 0:
            self.power = 1
            self.writestatus()
            t2 = self.enginestatuscheck()
        if self.offtime.hour == now.hour and self.offtime.minute == now.minute:
          if self.power == 1:
            self.fadeoff()
            self.power = 0
            self.writestatus()
  
  def run(self):
    c = sqlhelper.updatedicts()
    m,m2 = self.updatemodes()
    q = queue.Queue()
    t1 = threading.Thread(target=self.checkcodes,args=(q,))
    t1.daemon = True
    t1.start()
    delay = timedelta(milliseconds=1)
    then = datetime.now() + delay
    while True:
      now = datetime.now()
      if now > then:
        then = now + delay
        try:
          y = q.get()
          try:
            t2.do_run = False
          except: pass
          if y.get("power"):
            if int(y["power"]) == 0:
              self.fadeoff()
              self.power = 0
              self.writestatus()
              print("Power turned off")
            elif int(y["power"]) == 1:
              self.power = 1
              self.writestatus()
              t2 = self.enginestatuscheck()
              print("Power turned on")
          if y.get("sync"):
            self.sync = int(y["sync"])
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Sync updated")
          if y.get("shifter"):
            self.shifter = int(y["shifter"])
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Shifter updated")
          if y.get("colors"):
            z = y["colors"] 
            c = sqlhelper.updatedicts()
            self.shift3separate(z)
            self.power = 1
            self.program = 0
            self.writestatus()
            print("Colors updated")
          if y.get("color"):
            x = y["color"]
            self.shift(x)
            self.power = 1
            self.program = 0
            self.writestatus()
            print("Custom color")
          if y.get("bright"):
            self.bright = float(y["bright"])
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Brightness updated")
          if y.get("delay"):
            self.delay = float(y["delay"] )
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Delay updated")
          if y.get("mode"):
            m,m2 = self.updatemodes()
            self.mode = int(y["mode"])
            self.program = 1
            if self.mode in m2:
              t2 = threading.Thread(target=m[self.mode],args=(m2[self.mode],))
            else: t2 = threading.Thread(target=m[self.mode])
            t2.daemon = True
            t2.start()
            self.power = 1
            self.writestatus()
            print("Mode updated")
          if y.get("addmode"):
            u = y["addmode"] # will give list ["name","1,2,3"]
            sqlhelper.addmode(u[0],u[1])
            m,m2 = self.updatemodes()
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("New mode saved")
          if y.get("save"):
            u = y["save"] # will give list ["name","hexcode"]
            sqlhelper.addcolortodb(u[0],u[1])
            c = sqlhelper.updatedicts()
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("New color saved")
          if y.get("deletemode"):
            u = y["deletemode"] # will give hexcode string
            sqlhelper.deletemode(u)
            m,m2 = self.updatemodes()
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Mode removed")
          if y.get("delete"):
            u = y["delete"] # will give hexcode string
            sqlhelper.deletecolorfromdb(u)
            c = sqlhelper.updatedicts()
            self.writestatus()
            t2 = self.enginestatuscheck()
            print("Color removed")
          time.sleep(.1)
        except KeyboardInterrupt:
          print("KeyboardInterrupt")
          break
    try:
      t1.do_run = False
      t1.join()
      t2.do_run = False
      t2.join()
    except: pass

if __name__=="__main__":
  sys = System() #create object
  c = sqlhelper.updatedicts()
  # sys.turnon3separate([1,4,6])
  # time.sleep(1)
  # sys.turnoff() #turn off
  # sys.writestatus()
  sys.run() #start main program
  # sys.turnoff()
  # print("Done")

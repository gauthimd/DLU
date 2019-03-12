#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from application.config.base_config import DB_PATH

try:
  db = sqlite3.connect(DB_PATH)
  cur = db.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS status(
              id INTEGER PRIMARY KEY NOT NULL UNIQUE,
              program TEXT,
              delay TEXT,
              bright TEXT,
              lights TEXT,
              power TEXT,
              mode TEXT,
              shifter TEXT,
              sync TEXT,
              timerset TEXT,
              ontime TEXT,
              offtime TEXT,
              timestamp TEXT)
              ''')
  cur.execute('''CREATE TABLE IF NOT EXISTS commands(
              id INTEGER PRIMARY KEY NOT NULL UNIQUE,
              command TEXT,
              arg1 TEXT,
              arg2 TEXT,
              arg3 TEXT)
              ''')
  cur.execute('''CREATE TABLE IF NOT EXISTS colors(
              id INTEGER PRIMARY KEY NOT NULL UNIQUE,
              name TEXT UNIQUE,
              hexcode TEXT UNIQUE)
              ''')
  standardcolors = [("Red","#ff0000"),("Orange","#ff3200"),
                    ("Yellow","#d7c800"),("Green","#00ff00"),
                    ("Turquoise","#00ffff"),("Blue","#0000ff"),
                    ("Purple","#ff00ff"),("White","#ffffff")]
  cur.executemany('''INSERT INTO colors(name,hexcode) VALUES(?,?)''',
              standardcolors)
  cur.execute('''CREATE TABLE IF NOT EXISTS modes(
              id INTEGER PRIMARY KEY NOT NULL UNIQUE,
              name TEXT UNIQUE,
              mode TEXT,
              scheme TEXT UNIQUE)
              ''')
  modes = [("Siren",'holidays','1,6'),
           ("Cycle Colors",'holidays','1,2,3,4,5,6,7,8'),
           ("Valentines",'valentines',None),
           ("Christmas",'holidays','1,4,8'),
           ("4th of July",'holidays','1,8,6'),
           ("Cycle Random Color",'randomsync',None),
           ("Cycle Random Colors",'randomasync',None),
           ("Cycle Random Hues",'randomcolorasync',None)]
  cur.executemany('''INSERT INTO modes(name,mode,scheme) VALUES(?,?,?)''',
              modes)
  db.commit()
  db.close()
except Exception as e:
  raise e

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
from application.config.base_config import DB_PATH, PROGRAM
from Controls.sqlhelper import sqlhelper

while True:

    try:
        db = sqlite3.connect(DB_PATH)
        cur = db.cursor()
        cur.execute('''SELECT command,arg1,arg2,arg3,id FROM commands''')
        data = cur.fetchone()
        if data[0] == "colors":
            cur.execute('''UPDATE status set program=0''')
            cur.execute('''UPDATE status SET lights=?''', ('{} {} {}'.format(data[1], data[2], data[3]),))
            db.commit()
        elif data[0] == "save":
            u = [data[1], data[2]]
            x = {data[0]: u}  # sends "save" args as list of str ["name","hexcode"]
        else:
            if data[0] == 'power':
                cur.execute('UPDATE status SET power=?', (data[1],))
                db.commit()
            if data[0] == 'delay':
                cur.execute('UPDATE status SET delay=?', (data[1],))
                db.commit()
            if data[0] == 'bright':
                cur.execute('UPDATE status SET bright=?', (data[1],))
                db.commit()
            if data[0] == 'mode':
                cur.execute('''UPDATE status set program=1''')
                cur.execute('UPDATE status SET mode=?', (data[1],))
                db.commit()
            if data[0] == 'program':
                cur.execute('UPDATE status SET program=?', (data[1],))
                db.commit()
            if data[0] == 'shifter':
                cur.execute('UPDATE status SET shifter=?', (data[1],))
                db.commit()
            if data[0] == 'timerset':
                cur.execute('UPDATE status SET timerset=?', (data[1],))
                db.commit()
            if data[0] == 'offtime':
                cur.execute('UPDATE status SET offtime=?', (data[1],))
                db.commit()
            if data[0] == 'ontime':
                cur.execute('UPDATE status SET ontime=?', (data[1],))
                db.commit()
        cur.execute('''DELETE FROM commands''')
        db.commit()
        db.close()
    except Exception as e:
        pass

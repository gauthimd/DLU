import sqlite3
from Controls.colors import Color
from application.config.base_config import DB_PATH

class sqlhelper():

    def __init__(self):
        pass

    def readstatus(self):  # returns status dictionary
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT program,delay,bright,lights,power,mode,
                       shifter,sync,timerset,ontime,offtime,timestamp
                       FROM status ORDER BY id DESC LIMIT 1''')
            stat = cur.fetchone()
            try:
              z = stat[3].split()  # this puts the lights into a list
            except:
                z = stat[3]
            lights = []
            for i in z:
                lights.append(i)  # this makes lights a list of integers
            status = {"program": int(stat[0]), "delay": round(float(stat[1]), 1),
                      "bright": round(float(stat[2]), 2), "lights": lights,
                      "power": int(stat[4]), "mode": int(stat[5]),
                      "shifter": int(stat[6]), "sync": int(stat[7]), "timerset": int(stat[8]),
                      "ontime": stat[9], "offtime": stat[10], "timestamp": stat[11]}
            db.close()
        except Exception as e:
            status = {"error": 1}
            print('errored in readstatus: {}'.format(e))
        return status

    def updatedicts(self):  # these are what I use as configs
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT id, hexcode FROM colors''')
            rows = cur.fetchall()
            c = {}
            for row in rows:
                c[row[0]] = Color(row[1])  # gives dict {primary key:color object}
            db.close()
            return c
        except Exception as e:
            raise e

    def entercommand(self, command, arg1, arg2=None, arg3=None):
        try:  # args2 and 3 default to None, so only command and arg1 necessary
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''INSERT INTO commands(command,arg1,arg2,arg3) 
                  VALUES(?,?,?,?)''', (command, arg1, arg2, arg3))
            db.commit()
            db.close()
        except Exception as e:
            print('Excepted on entercommand', e)

    def writeupdate(self, update):  # RICKY DON'T USE THIS METHOD!!!! NOT FOR YOU!!!
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''INSERT INTO status(program, delay, bright, lights, power,
                     mode, shifter, sync, timerset, ontime, offtime, timestamp) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', update)
            cur.execute('''DELETE FROM status WHERE id NOT IN ( SELECT id FROM ( SELECT id FROM status ORDER BY id DESC LIMIT 10 ) foo )''')
            db.commit()
            db.close()
        except:
            pass

    def addcolortodb(self, name, hexcode):  # name and hexcode string, hexcode "#AA33FF"
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''INSERT INTO colors(name,hexcode) VALUES(?,?)''',
                        (name, hexcode))
            db.commit()
            db.close()
        except:
            pass  # names and hexcodes are unique, so trying to repeat values will get nada

    def deletecolorfromdb(self, hexcode):  # hexcode must be string of form "#FF23D6"
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT id FROM colors WHERE hexcode=?''', (hexcode,))
            row = cur.fetchone()
            status = self.readstatus()
            j = []
            for x in status["lights"]:
              try:
                j.append(int(x))
              except: pass
            if row[0] > 8 and row[0] not in j:
                cur.execute('''DELETE FROM colors WHERE hexcode=?''', (hexcode,))
                db.commit()
            else: print("Nope! Can't delete a color that is currently on.")
            db.close()
        except:
            pass

    def deletemode(self, modekey):
        try:
            modekey = int(modekey)
            status = self.readstatus()
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            if modekey > 8:
                if status["mode"] > 8 and status["program"] == 1: 
                    print('Cannot delete custom mode while any custom mode is on')
                else: 
                  cur.execute('''DELETE FROM modes WHERE id=?''', (modekey,))
                  db.commit()
            else: print('Cannot delete pre-existing modes')
            db.close()
        except Exception as e:
            print(e)

    def addmode(self, name, scheme):
        try:
            mode = 'holidays'
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''INSERT INTO modes(name, mode, scheme) 
                        VALUES(?,?,?)''',(name,mode,scheme))
            db.commit()
            db.close()
        except Exception as e:
            print(e)

    def getmodes(self):
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT * FROM modes''')
            rows = cur.fetchall()
            db.close()
            return rows
        except Exception as e:
            print('Excepted in getmodes', e)
            return None

    def getmodenames(self): #RICKY this is for you. Will return dict {1: "Siren", 2: "Cycle Colors",...}
        try:                #Use this after you add or delete modes
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT id,name FROM modes''')
            rows = cur.fetchall()
            db.close()
            modenamedict = {}
            for x in rows:
              modenamedict[x[0]] = x[1]
            return modenamedict
        except Exception as e:
            print('Error in getmodenames',e)
            return None

    def getcolors(self):
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT * FROM colors''')
            rows = cur.fetchall()
            db.close()
            return rows
        except Exception as e:
            print('Excepted in getcolors', e)
            return None

    def getcolorhex(self, color_id):
        try:
            db = sqlite3.connect(DB_PATH)
            cur = db.cursor()
            cur.execute('''SELECT hexcode FROM colors WHERE id=?''', (color_id,))
            row = cur.fetchone()
            # print('our rowboy', row)
            db.close()
            return row[0].replace('0x', '#')
        except Exception as e:
            print('Excepted in getcolorhex', e)
            return None

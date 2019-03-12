from colors import Color
import sqlite3
name = "orange"
try:
  db = sqlite3.connect('/home/pi/DockLights/Controls/db/data.db')
  cur = db.cursor()
  cur.execute('''SELECT hexcode FROM colors WHERE name=?''', (name,))
  row = cur.fetchone()
  myobj = Color(row[0])
except Exception as e:
  db.rollback()
  raise e
finally:
  db.close()
print myobj.greenpwm, myobj.redpwm

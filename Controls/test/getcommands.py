import sqlite3
conn = sqlite3.connect('/home/pi/DockLights/db/data.db')
cur = conn.cursor()
rows = cur.execute('SELECT command,arg1,arg2,arg3 FROM commands')
for row in rows:
    print(row)

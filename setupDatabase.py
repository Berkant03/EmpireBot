import sqlite3

conn = sqlite3.connect('empire.db')

cursor = conn.cursor()

cursor.execute("CREATE TABLE festungen (festung text primary key, fraktion text)")
cursor.execute("CREATE TABLE fraktionen (fraktion text primary key, rollen_id text, leiter_id text, leiter_name text, leiter_rollen_id text)") #Ids müssen Text sein, weil Discord IDs größer als das Integer-limit von sqlite sind!
cursor.execute("CREATE TABLE invasion (festung text, angreifer_fraktion text, verteidiger_fraktion text, datum text, uhrzeit text)")
cursor.execute("CREATE TABLE logs (person text, command text, channel text, datum text, uhrzeit text)")
conn.close()

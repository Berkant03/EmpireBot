import sqlite3

conn = sqlite3.connect('empire.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE festungen (festung TEXT PRIMARY KEY, fraktion TEXT,
                FOREIGN KEY (fraktion) REFERENCES fraktionen(fraktion))''')
cursor.execute("CREATE TABLE fraktionen (fraktion TEXT PRIMARY KEY, rollen_id TEXT, leiter_id TEXT, leiter_rollen_id TEXT)") #Ids müssen TEXT sein, weil Discord IDs größer als das Integer-limit von sqlite sind!
cursor.execute('''CREATE TABLE invasion (festung TEXT, angreifer_fraktion TEXT, verteidiger_fraktion TEXT, datum TEXT, uhrzeit TEXT,
                FOREIGN KEY (angreifer_fraktion) REFERENCES fraktionen(fraktion), FOREIGN KEY (verteidiger_fraktion) REFERENCES fraktionen(fraktion))''')
cursor.execute("CREATE TABLE logs (person TEXT, person_id TEXT, command TEXT, channel TEXT, datum TEXT, uhrzeit TEXT)") #Name und ID, um exploit durch renames zu verhindern



#Name, RollenID, LeiterID, LeiterRollenID
fraktionen = [("Nordmänner","587376412625731614","442350475950424104","587649118978179072"),
              ("Wilder Bergstamm","587376373849522257", "184385677301907456", "587648048641867776"),
              ("Piraten","587376215162355743","231855253564162049","587648225360740384"),
              ("Ägypter","587376337077927956","534021186439610389","587648422761463818"),
              ("Ureinwohner","587376464815456398","264177403188871178","587648931920347136"),
              ("Mystischer Orden","587376621846265896","367732762419003403","587648869551308801"),
              ("Römer","587376695691051017","339098056408432640","587648819680903171"),
              ("Dunkelritter","587376791170187274","351634859082645505","587648591548383232"),
              ("Samurai","587376876184666123","220558436037820417","587648705990098947")]

cursor.executemany("INSERT INTO fraktionen VALUES (?,?,?,?)",fraktionen)

festungen = [("1","Nordmänner"),
             ("Bergfort","Wilder Bergstamm"),
             ("2","Piraten"),
             ("3","Ägypter"),
             ("Wälder des Pantheon","Ureinwohner"),
             ("4","Mystischer Orden"),
             ("5","Römer"),
             ("6","Dunkelritter"),
             ("Kyoto","Samurai")]

cursor.executemany("INSERT INTO festungen VALUES (?,?)",festungen)

conn.close()

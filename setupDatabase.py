import sqlite3

conn = sqlite3.connect('empire.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE festungen (festung TEXT PRIMARY KEY, fraktion TEXT,
                FOREIGN KEY (fraktion) REFERENCES fraktionen(fraktion))''')
cursor.execute("CREATE TABLE fraktionen (fraktion TEXT PRIMARY KEY, rollen_id TEXT, leiter_id TEXT, leiter_rollen_id TEXT, nachricht TEXT)") #Ids müssen TEXT sein, weil Discord IDs größer als das Integer-limit von sqlite sind!
cursor.execute('''CREATE TABLE invasion (festung TEXT, angreifer_fraktion TEXT, verteidiger_fraktion TEXT, datum TEXT, uhrzeit TEXT,
                FOREIGN KEY (angreifer_fraktion) REFERENCES fraktionen(fraktion), FOREIGN KEY (verteidiger_fraktion) REFERENCES fraktionen(fraktion))''')
cursor.execute("CREATE TABLE logs (person TEXT, person_id TEXT, command TEXT, channel TEXT, datum TEXT, uhrzeit TEXT)") #Name und ID, um exploit durch renames zu verhindern
cursor.execute('''CREATE TABLE urlaub (fraktion TEXT PRIMARY KEY, urlaub TEXT,
                FOREIGN KEY (fraktion) REFERENCES fraktionen(fraktion))''')


#Name, RollenID, LeiterID, LeiterRollenID
fraktionen = [("Nordmänner","587376412625731614","442350475950424104","587649118978179072",'''Willkommen bei den Nordmännern!❄️
Du bist einer eisigen Fraktion beigetreten welche im Norden des Kontinents lebt.
Verhalte dich wie ein Nordmann! :santa: 
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Nordmann benehmen müsst!
Viel Spaß im Projekt! Auf ein eisiges Fest! ❄'''),
              ("Wilder Bergstamm","587376373849522257", "184385677301907456", "587648048641867776",'''Willkommen beim Wilden Bergstamm!:mount_fuji:
Du bist einer wilden Fraktion beigetreten welche in der nördlichen Zone des Kontinents lebt.
Verhalte dich wie ein Bewohner eines Wilden Stammes! :bear:
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Wilder benehmen müsst!
Viel Spaß im Projekt! Auf ein bergiges Fest!:mount_fuji:'''),
              ("Piraten","587376215162355743","231855253564162049","587648225360740384",'''Willkommen bei den Piraten!:skull:
Du bist einer trinkenden Fraktion beigetreten welche außerhalb des Kontinents auf einer steinigen Insel lebt.
Verhalte dich wie ein Pirat!
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Pirat benehmen müsst!
Sonst geht es auf die Planke!
Viel Spaß im Projekt! Arrr!:skull:'''),
              ("Ägypter","587376337077927956","534021186439610389","587648422761463818",'''Willkommen bei den Ägyptern!:sun_with_face:
Du bist einer weisen Fraktion beigetreten welche im Süden des Kontinents lebt.
Verhalte dich wie ein Ägypter! :small_red_triangle:
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ägypter benehmen müsst!
Viel Spaß im Projekt! Die Pyramiden sind mit dir!:sun_with_face:'''),
              ("Ureinwohner","587376464815456398","264177403188871178","587648931920347136",'''Willkommen bei den Ureinwohnern!:palm_tree:
Du bist einer alten und wilden Fraktion beigetreten welche in der süd-westlichen Zone des Kontinents lebt.
Verhalte dich wie ein Ureinwohner! :see_no_evil:
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ureinwohner benehmen müsst!
Viel Spaß im Projekt! Gepriesen sei der Baum!:palm_tree:'''),
              ("Mystischer Orden","587376621846265896","367732762419003403","587648869551308801",'''Willkommen bei dem mystischen Orden!:church:
Du bist einer geheimnisvollen Fraktion beigetreten welche in der Mitte des Kontinents lebt.
Verhalte dich entweder wie ein Händler Söldner oder Priester! ✝️
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Händler/Söldner/Priester benehmen müsst!
Auf ein spannendes Projekt!:church:'''),
              ("Mongolen","587376695691051017","339098056408432640","587648819680903171",'''Willkommen bei den Mongolen! :camel:
Du bist einer starken wilden Fraktion beigetreten welche im süd-östlichen des Kontinents lebt.
Verhalte dich wie ein Mongole!

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Mongole benehmen müsst!
Viel Spaß im Projekt! Auf eine friedliche oder düstere  Zeit! :camel:'''),
              ("Dunkelritter","587376791170187274","351634859082645505","587648591548383232",'''Willkommen bei den Dunkelrittern!:racehorse:
Du bist einer dunklen Fraktion beigetreten welche in der nord-östlichen Zone des Kontinents lebt.
Verhalte dich wie ein Dunkelritter du kannst natürlich auch ein Knappe oder ein Magier sein! :black_heart:
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ritter/Knappe/Magier benehmen müsst!
Viel Spaß im Projekt! Auf eine dunkle Zeit!:racehorse:'''),
              ("Samurai","587376876184666123","220558436037820417","587648705990098947",'''Willkommen bei den Samurai!:japanese_castle:
Du bist einer edlen Fraktion beigetreten welche im Westen des Kontinents lebt.
Verhalte dich wie ein Samurai! :dragon:
Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Samurai benehmen müsst!
Viel Spaß im Projekt! Auf das Jahr des Hundes!:japanese_castle:''')]

cursor.executemany("INSERT INTO fraktionen VALUES (?,?,?,?,?)",fraktionen)

festungen = [("Frosthammer","Nordmänner"),
             ("Bergfort","Wilder Bergstamm"),
             ("Gralsfestung","Piraten"),
             ("Anubrave#","Ägypter"),
             ("Wälder von Pantheon","Ureinwohner"),
             ("Medi Terra","Mystischer Orden"),
             ("Ulaanbataar#","Mongolen"),
             ("Umbra","Dunkelritter"),
             ("Kyoto","Samurai")]

cursor.executemany("INSERT INTO festungen VALUES (?,?)",festungen)

urlaub = [("Nordmänner","False"),
          ("Wilder Bergstamm","False"),
          ("Piraten","False"),
          ("Ägypter","False"),
          ("Ureinwohner","False"),
          ("Mystischer Orden","False"),
          ("Mongolen","False"),
          ("Dunkelritter","False"),
          ("Samurai","False")]

cursor.executemany("INSERT INTO urlaub VALUES(?,?)",urlaub)
conn.commit()
conn.close()

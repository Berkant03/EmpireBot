import sqlite3

conn = sqlite3.connect('empire.db')
cursor = conn.cursor()

def log(person_name,person_id,command,channel_name,datum): #command zeigt die volle message, datum als datetime.datetime object
    global cursor
    datum = str(datum).split()
    tag = datum[0]
    uhrzeit = datum[1][:5]
    cursor.execute("INSERT INTO logs VALUES (?,?,?,?,?,?)",[str(person_name),str(person_id),command,str(channel_name),tag,uhrzeit])
    conn.commit()

def festungsnamen_andern(fraktion,festung):
    global cursor
    cursor.execute("UPDATE festungen SET festung = ? WHERE fraktion = ?",[festung,fraktion])
    conn.commit()

def leiter_wechsel(fraktion,leiter_id): #Wenn sich der Leiter einer Stadt ändert
    global cursor
    cursor.execute("UPDATE fraktionen SET leiter_id = ? WHERE fraktion = ?",[leiter_id,fraktion])
    conn.commit()

def festung_einnahme(festung,fraktion): #Wenn eine Basis eingenommen wird. "fraktion" ist der neue Besitzer der Stadt
    global cursor
    cursor.execute("UPDATE festungen SET fraktion = ? WHERE festung = ?",[fraktion,festung])
    conn.commit()

def invasion_ankündigung(festung,angreifer_fraktion,verteidiger_fraktion,datum): #datum als datetime.datetime object
    global cursor
    datum = str(datum).split()
    tag = datum[0]
    uhrzeit = datum[1][:5]
    cursor.execute("INSERT INTO invasion VALUES (?,?,?,?,?)",[festung,angreifer_fraktion,verteidiger_fraktion,tag,uhrzeit])
    conn.commit()

def set_contest(fraktion,mode):
    global cursor
    cursor.execute("UPDATE contests SET contested = ? WHERE fraktion = ?",[mode,fraktion])
    conn.commit()

def set_urlaub(fraktion,mode):
    global cursor
    cursor.execute("UPDATE urlaub SET urlaub = ? WHERE fraktion = ?",[mode,fraktion])
    cursor.execute("UPDATE urlaub SET genutzt = ? WHERE fraktion = ?",["True",fraktion])
    conn.commit()

def set_urlaub_mit_datum(fraktion,mode,datum):
    global cursor
    cursor.execute("UPDATE urlaub SET urlaub = ? WHERE fraktion = ?",[mode,fraktion])
    cursor.execute("UPDATE urlaub SET genutzt = ? WHERE fraktion = ?",["True",fraktion])
    cursor.execute("UPDATE urlaub SET datum = ? WHERE fraktion = ?",[datum,fraktion])
    conn.commit()

def check_urlaub(fraktion):
    global cursor
    cursor.execute("SELECT urlaub FROM urlaub WHERE fraktion = ?",[fraktion])
    fff = cursor.fetchone()[0]
    if fff == "False":
        return False
    if fff == "True":
        return True

def urlauber():
    global cursor
    cursor.execute("SELECT fraktion,urlaub FROM urlaub")
    return "\n".join([x[0] + " : " +  x[1] for x in cursor.fetchall()])

def fraktions_liste():
    global cursor
    cursor.execute("SELECT fraktion FROM fraktionen")
    return "\n".join([x[0]  for x in cursor.fetchall()])

def contesteter():
    global cursor
    cursor.execute("SELECT fraktion, contested FROM contests")
    return "\n".join([x[0] + " : " +  x[1] for x in cursor.fetchall()])

def festungen():
    global cursor
    cursor.execute("SELECT festung,fraktion FROM festungen",)
    return "\n".join([x[0] + " : " +  x[1] for x in cursor.fetchall()])

def festungenZwei():
    global cursor
    cursor.execute("SELECT festung,fraktion FROM festungen",)
    return ",".join([x[0] + ":" +  x[1] for x in cursor.fetchall()])

def festungsNamen():
    global cursor
    cursor.execute("SELECT festung from festungen")
    return [x[0].lower() for x in cursor.fetchall()]

def invasions():
    global cursor
    cursor.execute("SELECT festung,angreifer_fraktion,verteidiger_fraktion,datum,uhrzeit FROM invasion")
    Inv_Txt = "\n".join(["Festung: "+x[0] + ", Angreifer: " +  x[1] + ",Verteidiger: " + x[2] + ", Datum: " + x[3] +", Uhrzeit: " +x[4] for x in cursor.fetchall()])
    if Inv_Txt == "":
        return "Es gibt keine Invasionen"
    else:
        return Inv_Txt

def fraktions_nachricht(fraktion): #Holt die Nachricht zu diesem fraktionsnamen raus
    global cursor
    cursor.execute("SELECT nachricht FROM fraktionen WHERE fraktion = ?",[fraktion])
    return cursor.fetchone()[0]
    #print(cursor.fetchone()[0])

def fraktions_nachricht_andern(fraktion,nachricht):
    global cursor
    cursor.execute("UPDATE fraktionen SET nachricht = ? WHERE fraktion = ?",[nachricht,fraktion])
    conn.commit()
    
def fraktions_namen_andern(alterName,neuerName):
    global cursor
    cursor.execute("UPDATE fraktionen SET fraktion = ? WHERE fraktion = ?",[neuerName,alterName])
    cursor.execute("UPDATE festungen SET fraktion = ? WHERE fraktion = ?",[neuerName,alterName])
    conn.commit()

def fraktionVonID(rolle_id):
    global cursor
    cursor.execute("SELECT fraktion FROM fraktionen WHERE rollen_id = ?",[rolle_id])
    return cursor.fetchone()[0]

def angreifer_fraktion_check(ang_frak):
    global cursor
    cursor.execute("SELECT angreifer_fraktion FROM invasion")
    ff = cursor.fetchall()
    #print([x[0] for x in cursor.fetchall()])
    #print(ang_frak)
    if ang_frak in [x[0] for x in ff]:
        #print(True)
        return True
    else:
        #print(False)
        return False


def reset_urlaub(fraktion):
    cursor.execute("UPDATE urlaub SET genutzt = ? WHERE fraktion = ?",["False",fraktion])
    conn.commit()
    

def invasions_check_alles(ang_frak,date,invDatum,ver_frak):
    global cursor
    invDatum = str(invDatum).split()[0]
    #print(invDatum)
    cursor.execute("SELECT angreifer_fraktion,verteidiger_fraktion FROM invasion WHERE datum = ?",[invDatum])    
    ang_ver_frak_list = cursor.fetchall()
    check_list = []
    for item in [x[0] for x in ang_ver_frak_list]:
        check_list.append(item)
    for item in [x[1] for x in ang_ver_frak_list]:
        check_list.append(item)
    
    if ang_frak in check_list:
        return False
    if ver_frak in check_list:
        return False

    """cursor.execute("SELECT angreifer_fraktion,verteidiger_fraktion FROM invasion WHERE datum > ?",[invDatum])
    ang_ver_list_spater = cursor.fetchall()
    check_list_zwei = []
    for item in [x[0] for x in ang_ver_list_spater]:
        check_list_zwei.append(item)
    for item in [x[1] for x in ang_ver_list_spater]:
        check_list_zwei.append(item)
    
    if ang_frak in check_list_zwei:
        return False
    if ver_frak in check_list_zwei:
        return False"""
    #print(check_list)

def angreifbar(ang_frak,ver_frak):
    global cursor
    cursor.execute("SELECT urlaub from urlaub WHERE fraktion = ?",[ang_frak])
    urlaub = cursor.fetchone()[0]
    #print(urlaub)
    if urlaub == "False":
        return False
    cursor.execute("SELECT urlaub FROM urlaub WHERE fraktion = ?",[ver_frak])
    urlaub_zwei = cursor.fetchone()[0]
    #print(urlaub_zwei)
    if urlaub_zwei == "False":
        return False
    return True

def contest_check(frakName):
    global cursor
    cursor.execute("SELECT contested FROM contests WHERE fraktion = ?",[frakName])
    if cursor.fetchone()[0] == "False":
        return False
    return True

def frakCheck(member):
    global cursor
    cursor.execute("SELECT rollen_id FROM fraktionen")
    rollenIDs = cursor.fetchall()
    rollenIDs = [int(x[0]) for x in rollenIDs]
    for item in [o.id for o in member.roles]:
        for z in rollenIDs:
            if item == z:
                return item

def delete_invasions(frakName,datum):
    global cursor
    cursor.execute("DELETE FROM invasion WHERE angreifer_fraktion = ? AND verteidiger_fraktion = ?",[frakName, frakName])
    conn.commit()
    

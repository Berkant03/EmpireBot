#Made by Berkant03 and MisterL2


import discord
from discord.utils import get
import time
import threading
import asyncio
import simplejson
import datetime
import math
import pyutil
import re
import sqlite3

TOKEN = ''

fraktionen = {"Dunkelritter":587938986262265859,"Wilder Bergstamm":587938913092370442,"Mystischer Orden":587939070353735730,"Nordmänner":587938861116817411,"Piraten":587939283701334016,"Ägypter":587939233902362634,"Ureinwohner":587939210644815882,"Mongolen":587939310414725140,"Samurai":587938954859249696}
allFractions = ["Dunkelritter","Wilder Bergstamm","Mystischer Orden","Nordmänner","Piraten","Ägypter","Ureinwohner","Mongolen","Samurai"]

conn = sqlite3.connect('empire.db')
cursor = conn.cursor()


leiter = [587649118978179072,587648048641867776,587648225360740384,587648422761463818,587648931920347136,587648869551308801,587648819680903171,587648591548383232,587648705990098947]
#Eisiger Mensch,Stammes Häuptling,Piratenkönig, Sultan,Ältester,Hoher Priester,König des Küstenvolkes,König der Dunkelritter,Kaiser
zuge = {587649118978179072:587376412625731614,#Eisiger Meister,Normänner
587648048641867776:587376373849522257,#Stammes Häuptling, Wilder Bergstamm
587648225360740384:587376215162355743,#Piratenkönig, Pirat
587648422761463818:587376337077927956,#Sultan, ägypter
587648931920347136:587376464815456398,#Ältester, Ureinwohner
587648869551308801:587376621846265896,#Hoher Priester, Mysticher Orden
587648819680903171:587376695691051017,#Kaiserin, Römer# ,Mongolen
587648591548383232:587376791170187274,#König der Dunkelritter, Dunkelritter
587648705990098947:587376876184666123}#Kaiser, Samurai

channels = {"fraktionswechsel":588769134158807243}

rollenID = {587376412625731614:"Nordmänner",
587376373849522257:"Wilder Bergstamm",
587376215162355743:"Piraten",
587376337077927956:"Ägypter",
587376464815456398:"Ureinwohner",
587376621846265896:"Mystischer Orden",
587376695691051017:"Mongolen",
587376791170187274:"Dunkelritter",
587376876184666123:"Samurai"}

rol = {"Dunkelritter":587376791170187274,"Samurai":587376876184666123,"Mongolen":587376695691051017,"Mystischer Orden":587376621846265896,
"Ureinwohner":587376464815456398,"Ägypter":587376337077927956,"Piraten":587376215162355743,"Wilder Bergstamm":587376373849522257,
"Nordmänner":587376412625731614}

tagForID = {0:"monday",1:"tuesday",2:"wednesday",3:"thursday",4:"friday",5:"saturday",6:"sunday"}
datetimetage = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
tageInEnglisch = {"samstag":"saturday","sonntag":"sunday"}
tageInDeutsch = {"monday":"montag","tuesday":"dienstag","wednesday":"mittwoch","thursday":"donnerstag","friday":"freitag","saturday":"samstag","sunday":"sonntag"}

#festungen = {"dunkelBurg":"Dunkelritter","palast":"Samurai","rom":"Römer","kirche":"Mystischer Orden","wälder das pantheon":"Ureinwohner",
#"pyramide":"Ägypter","boot":"Piraten","bergfort":"Wilder Bergstamm","eiskappen":"Nordmänner"}

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


def fraktionsnamen_parsen(name):
    if len(name) == 2:
        name = name[0] + " " + name[1]
    elif len(name) == 1:
        name = name[0]
    else:
        print("dafuq")
        raise Exception
    return name







async def giveRole(self,fraktion,payload):
        guild = self.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        await member.add_roles(discord.utils.get(guild.roles,name = fraktion),reason = "Fraktionsbeitritt",atomic=True)
        await member.remove_roles(discord.utils.get(guild.roles,name = "noch keine Fraktion"),reason = "Fraktionsbeitritt",atomic=True)
        await member.send(fraktions_nachricht(fraktion))
        channel = self.get_channel(channels["fraktionswechsel"])
        await channel.send(str(member)+" ist der Fraktion "+ str(fraktion) +" beigetreten")

async def check(self,payload):
    guild = self.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    for rolle in [f.name for f in member.roles]:
        if rolle in allFractions:
            await member.send("Du bist leider schon in einer Fraktion! Bitte kontaktiere die Projekt Leitung oder deinen Fraktionsleiter um aus deiner Fraktion auszutreten und somit einer neuen Beizutreten.")
            return True
    return False


    
async def authorcheck(self,autor,guild):
    for item in [z.id for z in autor.roles]:
        #print(item)
        if item in leiter:
            return True
    return False
    
async def fcheck(self,autor,guild,mention):
     #print(mention)
     for item in [a.id for a in autor.roles]:
         if item in leiter:
             for rolle in [r.id for r in mention.roles]:
                 if rolle == zuge[item]:
                     return rolle
             return False


def rollencheck(fraktion,member):
    for item in [z.id for z in member.roles]:
        if item == fraktion:
            return True
    return False

def frakCheck(member):
    global cursor
    cursor.execute("SELECT rollen_id FROM fraktionen")
    ffff = cursor.fetchall()
    ffff = [int(x[0]) for x in ffff]
    for item in [o.id for o in member.roles]:
        for z in ffff:
            if item == z:
                return item
#[<Guild id=564077511848493067 name='BT' shard_id=None chunked=True member_count=3>, <Guild id=579677389664157696 name='ðﾝﾕ﾿ðﾝﾖﾍðﾝﾖﾊ ðﾝﾕﾰðﾝﾖﾒðﾝﾖﾕðﾝﾖﾎðﾝﾖﾗðﾝﾖﾊ' shard_id=None chunked=True member_count=97>]


def delete_invasions(frakName,datum):
    global cursor
    cursor.execute("DELETE FROM invasion WHERE angreifer_fraktion = ? AND verteidiger_fraktion = ?",[frakName,frakName])
    conn.commit()
    
async def autocheck(self):
    guild = self.get_guild(579677389664157696)#THe empire discord
    channel = guild.get_channel(594852463727869952)#invasions-ankündigung
    while True:
        heute = datetime.datetime.now().date()
        """cursor.execute("SELECT festung,angreifer_fraktion,verteidiger_fraktion,datum,uhrzeit FROM invasion WHERE datum = ?",[str(heute)])
        x = cursor.fetchall()
        z = 0
        while z < len(x):
            k = x[z]
            print(k)
            festung = k[0]
            ang_fraktion = k[1]
            ver_fraktion = k[2]
            datum = k[3]
            uhrzeit = k[4]

            
            await asyncio.sleep(2)
            z += 1"""
        
        
        cursor.execute("UPDATE urlaub SET urlaub = ? WHERE datum = ?",["False",str(heute)])
        conn.commit()
        await asyncio.sleep(1800)


        #print(len(x))
        #print(x[0])
        #await asyncio.sleep(10)

class MyClient(discord.Client):
    global cursor
    async def on_member_join(self,member):
        await member.add_roles(discord.utils.get(member.guild.roles,name = "noch keine Fraktion"),reason = "Server Beitritt",atomic=True)
        await member.send("Willkommen bei The EMPRIE! Schau dir die Fraktionen in #die-fraktinoen an und wähle eine in #fraktionsbeitritt aus, um die Rolle zu erhalten!")
        
    async def on_ready(self):
        print('Logged on as', self.user)
        #await invasioncheck(self)
        #print(festungen())
        #print(festungsNamen())
        await autocheck(self)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower() == "!invasionen":
            await message.channel.send(invasions())
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content.startswith("!remove"):
            fraktion = frakCheck(message.author)
            frakName = fraktionVonID(str(fraktion))
            #if contest_check(frakName):
            #    await message.channel.send("Du wirst zurzeit herausgefordert, weshalb du ihn nicht entfernen kannst!")
            #    return
            for item in [j.id for j in message.mentions]:
                ausg = item
            person = message.guild.get_member(ausg)
            #print(person)
            #person = message.guild.get_member(message.mentions.id)
            if (await authorcheck(self,message.author,message.guild)):
                spieler = await fcheck(self,message.author,message.guild,person)
                if spieler == False:
                    await message.channel.send("Die Person die du rauswerfen möchtest, ist nicht in deiner Fraktion")
                else:
                    await person.remove_roles(message.guild.get_role(spieler),reason = "Fraktionsleiter hat ihn rausgeworfen",atomic=True)
                    #await message.channel.send(str(person.nick) + " wurde aus deiner Fraktion geworfen")
                    channel = self.get_channel(channels["fraktionswechsel"])
                    await channel.send(str(person) + " wurde aus der fraktion " +str(rollenID[spieler])+ " geworfen")
                    await person.add_roles(discord.utils.get(message.guild.roles,name = "noch keine Fraktion"),reason = "Aus der Fraktion geworfen",atomic=True)
                    log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
            
        if message.content.startswith("!request"):
            guild = message.guild
            author = message.author
            if (await authorcheck(self,author,guild)):
                msg = message.content
                channel = self.get_channel(589392821711011853)#requests
                await channel.send(str(author)+"'s Request: "+msg[8:])

        if message.content.lower() == "!playercount":
            await message.channel.send("Auf dem Server sind %s Mitglieder" % message.guild.member_count)
        
        if message.content.startswith("!pin"):
            if (await authorcheck(self,message.author,message.guild)):
                await message.pin()
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
        
        if message.content.startswith("!warte"):
            await asyncio.sleep(10)
            await message.channel.send("10 Sekunden sind um")
        
        if message.content.lower() == "!fraktionsverteilung":
            global fraktionen
            rollenanzahl = {name:0 for name in fraktionen.keys()}
            
            for member in message.guild.members:
                for rolle in rollenanzahl.keys():
                    rollenanzahl[rolle] += rollencheck(rol[rolle],member)
                    
                    
            nachricht = "\n".join([f"{rolle}: {rollenanzahl[rolle]}" for rolle in rollenanzahl])
            await message.channel.send(nachricht)
            
        if message.content.startswith("!invasion"):
            if re.fullmatch("!invasion [\w\s]+, (Samstag|Sonntag) \\d\\d:\\d\\d",message.content) is None:
                await message.channel.send("error!")
                return #keinen weiteren code ausführen

            guild = message.guild
            author = message.author
            if (await authorcheck(self,author,guild)):

                splitmsg = message.content[10:].lower().split(",")
                #print(splitmsg)
                festung = splitmsg[0]
                #print(festung)
                if festung not in festungsNamen():
                    await message.channel.send("festung gibts nicht")
                    return #keinen weiteren code ausführen
                splitmsg = splitmsg[1][1:].split(" ")
                #print(splitmsg)
                tag = splitmsg[0]
                #print(tag)
                splitmsg = splitmsg[1].split(":")
                #print(splitmsg)
                uhrzeit = datetime.time(int(splitmsg[0]),int(splitmsg[1]))
                #print(uhrzeit)
                stunde =splitmsg[0]
                minute = splitmsg[1]
                nachricht = message.content[9:].lower().strip()
                #print(nachricht)
                fraktion = await fcheck(self,message.author,message.guild,message.author)
                frakName = fraktionVonID(str(fraktion))
                #print(frakName)
                nachricht= nachricht +","+str(guild.get_role(fraktion).name)+"\n"
                #print(nachricht)

                #date
                heuteZeit = datetime.datetime.now()
                heute = datetime.datetime.now().date()
                InvtagID = datetimetage[tageInEnglisch[tag]]
                InvMonat = heute.month
                heuteTag = heute.weekday()
                # tagForID[heuteTag]    #tag in englisch
                #print(heute)
                #print(InvtagID)
                #print(tagForID[heuteTag])

                tagDifferenz = InvtagID - heuteTag
                print(tagDifferenz)
                InvJahr = heute.year
                InvMonat = int(heute.month)
                
                InvDelta = datetime.timedelta(days=tagDifferenz)
                InvDatum = heute + InvDelta

                
                #InvDatum = str(datetime.datetime(InvJahr,InvMonat,InvTag)).split()[0]
                InvStunde = int(stunde)
                
                if tagDifferenz == 0:
                    nowSek = int(heuteZeit.hour)*3600+int(heuteZeit.minute)*60
                    invSek = InvStunde*3600+ int(minute)*60
                    if (invSek - nowSek < 72000):
                        await message.channel.send("Eine Invasion muss 20 Stunden vor Beginn angekündigt werden")
                        return

                #print(InvDatum)
                #print(InvStunde)
                #print(minute)


                if int(InvStunde) < 16 or int(InvStunde) > 22:
                    await message.channel.send("Der Server ist um %s Uhr nicht offen. Bitte wähle eine andere Uhrzeit" % InvStunde)
                    return
                
                #print(festungenZwei().split(","))
                #invasion_ankündigung(festung,frakName,)
                festungenFraktionen = {}
                fraktionenFestungen = {}
                for item in festungenZwei().split(","):
                    item = item.split(":")
                    festungenFraktionen.update( {item[0].lower():item[1]} )
                    fraktionenFestungen.update( {item[1]:item[0]})
                #print(festungenFraktionen)
                verteidigendeFraktion = festungenFraktionen[festung]
                #print(verteidigendeFraktion)
                festung = fraktionenFestungen[verteidigendeFraktion]
                #print(festung)
                #print(frakName)
                #print(InvDatum)
                
                InvDatum = datetime.datetime(InvDatum.year,InvDatum.month,InvDatum.day,int(stunde),int(minute))

                if InvDatum.date() < heute:
                    await message.channel.send("Du kannst Invasionen erst in der Woche in der sie stattfinden sollen ankündigen")
                    return
                if invasions_check_alles(frakName,heute,InvDatum,verteidigendeFraktion) == False:
                    await message.channel.send("Du kannst keine Invasion starten da du schon in eine Invasion verwickelt bist oder die Festung/Fraktion die du angreifen möchtest dies ebenfalls zu seien scheint")
                    return
                #print(InvDatum)
                
                if angreifbar(frakName,verteidigendeFraktion):
                    await message.channel.send("Die Fraktion von dir oder die Fraktion die du angreifen möchtest ist dieses Wochende im Urlaub")
                    return

                #if contest_check(frakName):
                #    await message.channel.send("Du wirst zurzeit herausgefordert, weshalb du keine Invasion starten kannst")
                #   return

                if check_urlaub(frakName):
                    await message.channel.send("Du bist zurzeit im Urlaub und kannst nicht bei Invasionen Teilnehmen")
                    return
                
                if check_urlaub(verteidigendeFraktion):
                    await message.channel.send("Die Fraktion die du angreifen möchtest ist im Urlaub!")
                    return
                invasion_ankündigung(festung,frakName,verteidigendeFraktion,InvDatum)

                #pings
                ang_frak_ping = message.guild.get_role(rol[frakName]).mention
                ver_frak_ping = message.guild.get_role(rol[verteidigendeFraktion]).mention
                channel = message.guild.get_channel(594852463727869952)#ankündingungen
                await channel.send("Die Fraktion %s hat eine Invasion auf die Festung %s der Fraktion %s angekündigt. Die Invasion finden am %s.%s.%s um %s:%s Uhr statt!" % (ang_frak_ping,festung, ver_frak_ping, InvDatum.date().day,InvDatum.date().month,InvDatum.date().year,InvDatum.hour,str(InvDatum.time()).split(":")[1]))
                
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                await message.channel.send("Erfolgreich")

        if message.content.lower() == "!urlaub":
            guild = message.guild
            author = message.author
            if (await authorcheck(self,author,guild)):
                fraktion = await fcheck(self,author,guild,author)
                frakName = fraktionVonID(str(fraktion)) 
                #if contest_check(frakName):   
                #    await message.channel.send("Du wirst zurzeit herausgefordert, weshalb du keinen Urlaub starten kannst")
                #    return
                
                cursor.execute("SELECT genutzt FROM urlaub WHERE fraktion = ?",[frakName])
                if cursor.fetchone()[0] == "True":
                    await message.channel.send("Du kannst keinen Urlaub einschalten, weil du den Urlaub schonmal genutzt hast!")
                    return
                #set_urlaub(frakName,"True")
                #set_urlaub_mit_datum(frakName,"True",str(datetime.datetime.now().date()))
                
                cursor.execute("DELETE FROM invasion WHERE angreifer_fraktion = ? OR verteidiger_fraktion = ?",[frakName,frakName])
                conn.commit()
                #date

                #Aktueller Tag inklusive + 6 Folgetage (inkl)
                heute = datetime.datetime.now().date()
                delta = datetime.timedelta(days=6)
                urlaubsdatum = heute + delta
                set_urlaub_mit_datum(frakName,"True",str(urlaubsdatum))
                
                #Im channel für Invasionen, Rebellionen, Urlaube, etc.
                await message.guild.get_channel(594852463727869952).send(f"Die Fraktion {message.guild.get_role(fraktion).mention} ist bis zum {str(urlaubsdatum)} im Urlaub. In dieser Zeit sind keine Invasionen oder Rebellionen möglich!")

        if message.content.lower() == "!fraktionen":
            await message.channel.send(fraktions_liste())
        
        if message.content.lower() == "!urlauber":
            await message.channel.send(urlauber())

        if message.content == "!testpingme":
            await message.channel.send("%s" % message.author.mention)
        
        if message.content == "!festungen":
            await message.channel.send(festungen())
        
        if message.content.lower() == "!contest":
            fraktion = frakCheck(message.author)
            frakName = fraktionVonID(str(fraktion))
            cursor.execute("SELECT contested FROM contests WHERE fraktion = ?",[frakName])
            if cursor.fetchone()[0] == "True":
                await message.channel.send("Dein Fraktionsleiter kann nicht herausgefordert werden, weil ihn schon jemand anderes herausgefordert hat")
                return
            cursor.execute("SELECT leiter_rollen_id FROM fraktionen WHERE rollen_id = ?",[fraktion])
            leiter_rollen_id = cursor.fetchone()[0]
            print(frakName)
            print(leiter_rollen_id)
            for member in message.guild.members:
                if int(leiter_rollen_id) in [j.id for j in member.roles]:
                    contested = member.id
                    await message.channel.send("%s fordert seinen Fraktionsleiter %s zu einem Kampf um die Führungsposition auf. Währenddessen kann der jetzige Fraktionsleiter weder !remove oder !urlaub nutzen!" % (message.author.mention,member.mention))
            
            await message.guild.get_member(contested).remove_roles(message.guild.get_role(int(leiter_rollen_id)),reason="Contest",atomic=True)
            await message.guild.get_member(contested).remove_roles(message.guild.get_role(587954721856421888),reason="Contest",atomic=True)
            #set_contest(frakName,"True")

            cursor.execute("UPDATE contests SET contested_id = ? WHERE fraktion = ?",[str(contested),frakName])
            conn.commit()
            cursor.execute("UPDATE contests SET contestor_id = ? WHERE fraktion = ?",[str(message.author.id),frakName])
            conn.commit()

        if message.content.lower() == "!uncontest":
            fraktion = frakCheck(message.author)
            frakName = fraktionVonID(str(fraktion))
            cursor.execute("SELECT contested_id FROM contests WHERE fraktion = ?",[frakName])
            contested = cursor.fetchone()[0]
            cursor.execute("SELECT contestor_id FROM contests WHERE fraktion = ?",[frakName])
            contestor = cursor.fetchone()[0]

            if message.author.id == int(contested) or message.author.id == int(contestor):
                set_contest(frakName,"False")
                await message.channel.send("Herausforderung ist beendet")
            else:
                await message.channel.send("Du bist nicht der Fraktionsleiter oder der der ihn Herausfordert!")

        if message.content.lower() == "!contestete":
            await message.channel.send(contesteter()) 

        if message.content in ["!help","!hilfe"]:
            hilfe = """**----------Commands für Nutzer----------**
!playercount
!fraktionsverteilung
!festungen
!fraktionslose
!leave
!festungen
!urlauber
!invasionen
**----------Commands für Könige/Fraktionsleiter----------**
!invasion Festung, Samstag/Sonntag hh:mm
!remove @<player>
!request <text>
!add @<player>
!urlaub
**----------Commands für Projektleitung/Developer---------**
!fraktionsnamenändern , <alterFraktionsname> , <NeuerFraktionsname>
!fraktionsnachrichtändern , <Fraktion> , <Nachricht>
!festungsnamenändern, <Fraktion>,<neuerFestungsName>
!purge <anzahl>
!unurlaub, <fraktion>
!reseturlaub, <fraktion>"""
            await message.channel.send(hilfe)
            
                    
        
        if message.content.startswith("!add"):
            cursor.execute("SELECT leiter_rollen_id FROM fraktionen")
            lrid = [x[0] for x in cursor.fetchall()]#Put Tuple values into List               
            for rollen in lrid:
                if int(rollen) in [h.id for h in message.author.roles]:                   
                    cursor.execute("SELECT rollen_id FROM fraktionen WHERE leiter_rollen_id = ?",[rollen])#Get rollen_id
                    ID = cursor.fetchone()[0]#Get Tuple Value
                    ID = int(ID)
                    user = message.mentions[0]
                    if 587406516567539801 in [h.id for h in message.guild.get_member(user.id).roles]:
                        await user.add_roles(message.guild.get_role(ID),reason = "Fraktionsbeitritt durch Könige",atomic=True)
                        await user.remove_roles(message.guild.get_role(587406516567539801),reason ="Fraktionsbeitritt durch Könige",atomic=True)
                        await message.channel.send(str(user)+ " wurde der fraktion hinzugefügt!")
                        log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
         
        if message.content.lower() == "!fraktionslose":
            fraktionslose = 0
            for member in message.guild.members:
                if 587406516567539801 in [o.id for o in member.roles]:
                    fraktionslose += 1
            await message.channel.send("Auf dem Server haben %s Personen noch keine Fraktion" % fraktionslose)
         
        if message.content.lower().startswith("!purge"):
            anzahl = message.content.split()
            def check(m):
                return m.content and m.channel
            for r in [b.id for b in message.author.roles]:
                if r in [579701404289990685,587711467793678350,587939760878780416]:
                    msd = await message.channel.send("Bist du dir Sicher? Antworte mit ja oder nein!")
                    msg = await self.wait_for('message',check=check)
                    if msg.content.lower() == "ja":
                        log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                        await message.delete()
                        await msd.delete()
                        await msg.delete()
                        await msg.channel.purge(limit=int(anzahl[1]))
                    elif msg.content.lower() == "nein":
                        await msg.channel.send("Abgebrochen")
        
        if message.content.lower() == "!givedeveloper":#Für Testzwecke falls ich den Server leave dann kann ich mir diese Rolle wiedergeben
            if message.author.id == 235492603028570112:
                await message.author.add_roles(message.guild.get_role(587939760878780416),reason = "Ich bin Berkant darum xD",atomic=True)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
        
        if message.content.startswith("!fraktionsnachrichtändern"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                frak = fraktionsnamen_parsen(msg.split(",")[1].split())
                txt = msg.split(", ")[2]
                fraktions_nachricht_andern(frak,txt)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                
        
        if message.content.startswith("!fraktionsnamenändern"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                
                alter_name = fraktionsnamen_parsen(msg.split(",")[1].split())
                neuer_name = fraktionsnamen_parsen(msg.split(",")[2].split())

                
                fraktions_namen_andern(alter_name,neuer_name)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())

        if message.content.startswith("!unurlaub"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                fraktion = fraktionsnamen_parsen(msg.split(",")[1].split())
                cursor.execute("SELECT fraktion FROM fraktionen")
                xxxx = cursor.fetchall()
                xxxx = [x[0] for x in xxxx]
                if not(fraktion in xxxx):
                    await message.channel.send("Diese Fraktion gibt es nicht!")
                    return
                set_urlaub(fraktion,"False")
                await message.channel.send("Die Fraktion %s wurde aus ihrem Urlaub gezogen!" % fraktion)

        if message.content.startswith("!reseturlaub"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                fraktion = fraktionsnamen_parsen(msg.split(",")[1].split())
                cursor.execute("SELECT fraktion FROM fraktionen")
                alle_fraktionen = cursor.fetchall()
                alle_fraktionen = [x[0] for x in alle_fraktionen]
                #print(fraktion)
                if not(fraktion in alle_fraktionen):
                    await message.channel.send("Diese Fraktion gibt es nicht!")
                    return

                reset_urlaub(fraktion)
                # cursor.execute("UPDATE urlaub SET genutzt = ? WHERE fraktion = ?",["False",fraktion])
                # conn.commit()
                await message.channel.send("Urlaub der Fraktion %s wurde resettet" % fraktion)

        if message.content.startswith("!festungsnamenändern"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                
                fraktion = fraktionsnamen_parsen(msg.split(",")[1].split())
                newFestName = fraktionsnamen_parsen(msg.split(",")[2].split())
                
                #print(newFestName)
                festungsnamen_andern(fraktion,newFestName)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                await message.channel.send("Erfolgreich")
        
        if message.content.lower() == "!leave":
            for item in [k.id for k in message.author.roles]:
                if item in rollenID.keys():
                    await message.author.remove_roles(message.guild.get_role(item),reason = "!leave", atomic = True)
                    await message.author.add_roles(message.guild.get_role(587406516567539801),reason = "!leave",atomic = True)
                    channel = self.get_channel(channels["fraktionswechsel"])
                    await channel.send(str(message.author) + " ist aus seiner Fraktion ausgetreten")
                    log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
        
    async def on_raw_reaction_add(self,payload):
        if payload.channel_id == 587938281052700683:            
            if payload.message_id == fraktionen["Mystischer Orden"]: #Heiliger Orden
                if not (await check(self,payload)):
                    #await giveRole(self,"Mystischer Orden",payload)
                    guild = self.get_guild(payload.guild_id)
                    #message = guild.get_message(payload.message_id)
                    spieler = guild.get_member(payload.user_id)
                    await spieler.send("Um dem Mystischem Orden beizutreten musst du dich bei @Dr_EckigLP#8801 melden")
                    return
                    
            for fraktionsname in ["Nordmänner","Piraten","Ägypter","Ureinwohner","Mongolen","Samurai","Dunkelritter","Wilder Bergstamm"]:
                if payload.message_id == fraktionen[fraktionsname]:
                    if not (await check(self,payload)):
                        await giveRole(self,fraktionsname,payload)
                        return


client = MyClient()
client.run(TOKEN)

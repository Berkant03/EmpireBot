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
from calendar import monthrange

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


def festungen():
    global cursor
    cursor.execute("SELECT festung,fraktion FROM festungen",)
    return ",\n".join([x[0] + ":" +  x[1] for x in cursor.fetchall()])

def festungenZwei():
    global cursor
    cursor.execute("SELECT festung,fraktion FROM festungen",)
    return ",".join([x[0] + ":" +  x[1] for x in cursor.fetchall()])

def festungsNamen():
    global cursor
    cursor.execute("SELECT festung from festungen")
    return [x[0].lower() for x in cursor.fetchall()]

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
    if ang_frak in [x[0] for x in cursor.fetchall()]:
        return True
    else:
        return False

def angreifer_fraktion_check_datum(ang_frak,datum):
    global cursor
    cursor.execute("SELECT datum FROM invasion WHERE angreifer_fraktion = ?",[ang_frak])
    if str(datum) == str(cursor.fetchone()[0]):
        return True
    else:
        return False

def verteidiger_fraktion_check(ver_frak):
    global cursor
    cursor.execute("SELECT verteidiger_fraktion FROM invasion")
    if ver_frak in [x[0] for x in cursor.fetchall()]:
        return True
    else:
        return False

def verteidiger_fraktion_check_datum(ver_frak,datum):
    global cursor
    cursor.execute("SELECT datum FROM invasion WHERE verteidiger_fraktion = ?",[ver_frak])
    if str(datum) == str(cursor.fetchone()[0]):
        return True
    else:
        return False

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
            
#[<Guild id=564077511848493067 name='BT' shard_id=None chunked=True member_count=3>, <Guild id=579677389664157696 name='ðﾝﾕ﾿ðﾝﾖﾍðﾝﾖﾊ ðﾝﾕﾰðﾝﾖﾒðﾝﾖﾕðﾝﾖﾎðﾝﾖﾗðﾝﾖﾊ' shard_id=None chunked=True member_count=97>]


class MyClient(discord.Client):
    async def on_member_join(self,member):
        await member.add_roles(discord.utils.get(member.guild.roles,name = "noch keine Fraktion"),reason = "Server Beitritt",atomic=True)
        await member.send("Willkommen bei The EMPRIE! Schau dir die Fraktionen in #die-fraktinoen an und wähle eine in #fraktionsbeitritt aus, um die Rolle zu erhalten!")
        
    async def on_ready(self):
        print('Logged on as', self.user)
        #await invasioncheck(self)
        #print(festungen())
        #print(festungsNamen())

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        
        if message.content.startswith("!remove"):
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
                

                if monthrange(heute.year,heute.month)[1] < (heute.day + tagDifferenz):
                    u = (heute.day + tagDifferenz) - monthrange(heute.year,heute.month)[1] 
                    InvMonat += 1
                    InvTag = u
                    InvJahr = heute.year
                elif monthrange(heute.year,heute.month)[1] > (heute.day + tagDifferenz):
                    u = heute.day + tagDifferenz 
                    InvMonat = heute.month
                    InvTag = u
                    InvJahr = heute.year
                
                InvDatum = str(datetime.datetime(InvJahr,InvMonat,InvTag)).split()[0]
                InvStunde = stunde
                
                if tagDifferenz == 0:
                    nowSek = heuteZeit.hour*3600+heuteZeit*60
                    invSek = InvStunde*3600+ minute*60
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
                if angreifer_fraktion_check(frakName) and angreifer_fraktion_check_datum(frakName,InvDatum):
                    await message.channel.send("Deine Fraktion greift schon jemanden an")
                    return
                if verteidiger_fraktion_check(frakName) and verteidiger_fraktion_check_datum(frakName,InvDatum):
                    await message.channel.send("Deine Fraktion wird angegriffen, weshalb du keine Invasion Starten kannst")
                    return
                if angreifer_fraktion_check(verteidigendeFraktion) and angreifer_fraktion_check_datum(verteidigendeFraktion,InvDatum):
                    await message.channel.send("Die Fraktion die du angreifen möchtest, greift schon jemand anderes an")
                    return
                if verteidiger_fraktion_check(verteidigendeFraktion) and verteidiger_fraktion_check_datum(verteidigendeFraktion,InvDatum):
                    await message.channel.send("Die Fraktion die du angreifen möchtest, verteidigt schon jemanden anderes")
                    return

                InvDatum = datetime.datetime(InvJahr,InvMonat,InvTag,int(stunde),int(minute))
                #print(InvDatum)
                invasion_ankündigung(festung,frakName,verteidigendeFraktion,InvDatum)

                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                #archivieren(nachricht)# Muss noch gemacht werden TODO
                
                
        
        if message.content == "!festungen":
            global cursor
            await message.channel.send(festungen())
            
        
        if message.content in ["!help","!hilfe"]:
            hilfe = """----------Commands für Nutzer----------
!playercount
!fraktionsverteilung
!festungen
!fraktionslose
!leave
----------Commands für Könige/Fraktionsleiter----------
!invasion Festung, Samstag/Sonntag hh:mm
!remove @<player>
!request <text>
!add @<player>
----------Commands für Projektleitung/Developer---------
!fraktionsnamenändern , <alterFraktionsname> , <NeuerFraktionsname>
!fraktionsnachrichtändern , <Fraktion> , <Nachricht>"""
            await message.channel.send(hilfe)
            
                    
        
        if message.content.startswith("!add"):
            global cursor
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
                frak = msg.split(",")[1].split()
                if len(frak) == 2:
                    frak = frak[0] + " " + frak[1]
                elif len(frak) == 1:
                    frak = frak[0]
                txt = msg.split(", ")[2]
                fraktions_nachricht_andern(frak,txt)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
                
        
        if message.content.startswith("!fraktionsnamenändern"):
            if message.author.id in [521087967402655767,184385677301907456,442350475950424104,235492603028570112]:
                msg = message.content
                
                alterName = msg.split(",")[1].split()
                if len(alterName) == 2:
                    alterName = alterName[0] + " " + alterName[1]
                elif len(alterName) == 1:
                    alterName = alterName[0]
                
                neuerName = msg.split(",")[2].split()
                if len(neuerName) == 2:
                    neuerName = neuerName[0] + " " + neuerName[1]
                elif len(neuerName) == 1:
                    neuerName = neuerName[0]
                
                fraktions_namen_andern(alterName,neuerName)
                log(message.author,message.author.id,message.content,message.channel,datetime.datetime.now())
        
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
            if payload.message_id == fraktionen["Dunkelritter"]: #Dunkelritter
                if not (await check(self,payload)):
                    await giveRole(self,"Dunkelritter",payload)

            if payload.message_id == fraktionen["Wilder Bergstamm"]:
                if not (await check(self,payload)):
                    await giveRole(self,"Wilder Bergstamm",payload)
            
            if payload.message_id == fraktionen["Mystischer Orden"]: #Heiliger Orden
                if not (await check(self,payload)):
                    #await giveRole(self,"Mystischer Orden",payload)
                    guild = self.get_guild(payload.guild_id)
                    #message = guild.get_message(payload.message_id)
                    spieler = guild.get_member(payload.user_id)
                    await spieler.send("Um dem Mystischem Orden beizutreten musst du dich bei @Dr_EckigLP#8801  melden")
                    
            if payload.message_id == fraktionen["Nordmänner"] : #Nordmänner
                if not (await check(self,payload)):
                    await giveRole(self,"Nordmänner",payload)

            if payload.message_id == fraktionen["Piraten"] : #Piraten
                if not (await check(self,payload)):
                    await giveRole(self,"Piraten",payload)

            if payload.message_id == fraktionen["Ägypter"] : #Wüstenvolk
                if not (await check(self,payload)):
                    await giveRole(self,"Ägypter",payload)

            if payload.message_id == fraktionen["Ureinwohner"] : #Ureinwohner
                if not (await check(self,payload)):
                    await giveRole(self,"Ureinwohner",payload)

            if payload.message_id == fraktionen["Mongolen"] : #Küstenvolk/Römer
                if not (await check(self,payload)):
                   await giveRole(self,"Mongolen",payload)

            if payload.message_id == fraktionen["Samurai"] : #Samurai
                if not (await check(self,payload)):
                    await giveRole(self,"Samurai",payload)



client = MyClient()
client.run(TOKEN)

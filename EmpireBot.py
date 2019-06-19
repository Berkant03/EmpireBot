#Made by Berkant03 and MisterL2
#Email: berkantpalazoglu03@gmail.com

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

TOKEN = 'Your Token'

fraktionen = {"Dunkelritter":587938986262265859,"Wilder Bergstamm":587938913092370442,"Mystischer Orden":587939070353735730,"Nordmänner":587938861116817411,"Piraten":587939283701334016,"Ägypter":587939233902362634,"Ureinwohner":587939210644815882,"Römer":587939310414725140,"Samurai":587938954859249696}
allFractions = ["Dunkelritter","Wilder Bergstamm","Mystischer Orden","Nordmänner","Piraten","Ägypter","Ureinwohner","Römer","Samurai"]
nachricht = {"Dunkelritter":"""Willkommen bei den Dunkelrittern!:racehorse:
Du bist einer dunklen Fraktion beigetreten welche in der nord-östlichen Zone des Kontinents lebt.
Verhalte dich wie ein Dunkelritter du kannst natürlich auch ein Knappe oder ein Magier sein! :black_heart:

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ritter/Knappe/Magier benehmen müsst!
Viel Spaß im Projekt! Auf eine dunkle Zeit!:racehorse:""",
"Wilder Bergstamm":"""Willkommen beim Wilden Bergstamm!:mount_fuji:
Du bist einer wilden Fraktion beigetreten welche in der nördlichen Zone des Kontinents lebt.
Verhalte dich wie ein Bewohner eines Wilden Stammes! :bear:

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Wilder benehmen müsst!
Viel Spaß im Projekt! Auf ein bergiges Fest!:mount_fuji:""",
"Mystischer Orden":"""Willkommen bei dem mystischen Orden!:church:
Du bist einer geheimnisvollen Fraktion beigetreten welche in der Mitte des Kontinents lebt.
Verhalte dich entweder wie ein Händler Söldner oder Priester! ✝️

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Händler/Söldner/Priester benehmen müsst!
Auf ein spannendes Projekt!:church:""",
"Nordmänner":"""Willkommen bei den Nordmännern!❄️
Du bist einer eisigen Fraktion beigetreten welche im Norden des Kontinents lebt.
Verhalte dich wie ein Nordmann! :santa: 

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Nordmann benehmen müsst!
Viel Spaß im Projekt! Auf ein eisiges Fest! ❄️""",
"Piraten":"""Willkommen bei den Piraten!:skull:
Du bist einer trinkenden Fraktion beigetreten welche außerhalb des Kontinents auf einer steinigen Insel lebt.
Verhalte dich wie ein Pirat!

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Pirat benehmen müsst!
Sonst geht es auf die Planke!
Viel Spaß im Projekt! Arrr!:skull:""",
"Ägypter":"""Willkommen bei den Ägyptern!:sun_with_face:
Du bist einer weisen Fraktion beigetreten welche im Süden des Kontinents lebt.
Verhalte dich wie ein Ägypter! :small_red_triangle:

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ägypter benehmen müsst!
Viel Spaß im Projekt! Die Pyramiden sind mit dir!:sun_with_face:""",
"Ureinwohner":"""Willkommen bei den Ureinwohnern!:palm_tree:
Du bist einer alten und wilden Fraktion beigetreten welche in der süd-westlichen Zone des Kontinents lebt.
Verhalte dich wie ein Ureinwohner! :see_no_evil:

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Ureinwohner benehmen müsst!
Viel Spaß im Projekt! Gepriesen sei der Baum!:palm_tree:""",
"Samurai":"""Willkommen bei den Samurai!:japanese_castle:
Du bist einer edlen Fraktion beigetreten welche im Westen des Kontinents lebt.
Verhalte dich wie ein Samurai! :dragon:

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Samurai benehmen müsst!
Viel Spaß im Projekt! Auf das Jahr des Hundes!:japanese_castle:""",
"Römer":"""Willkommen bei den Römern!:ocean:
Du bist einer eigentlich friedlichen Fraktion beigetreten welche im süd-östlichen des Kontinents lebt.
Verhalte dich wie ein Römer!

Das hier ist ein Fulltime Roleplay Projekt das heißt ihr spielt einen Charakter. 
Welche Eigenschaften der Charakter hat ist euch überlassen. Ihr dürft also euch selbst spielen 
ABER beachtet das ihr in einer Fraktion seid und ihr euch wie ein Römer benehmen müsst!
Viel Spaß im Projekt! Auf eine friedliche oder düstere Zeit!:ocean:"""}

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
587648819680903171:587376695691051017,#Kaiserin, Römer
587648591548383232:587376791170187274,#König der Dunkelritter, Dunkelritter
587648705990098947:587376876184666123}#Kaiser, Samurai

channels = {"fraktionswechsel":588769134158807243}

rollenID = {587376412625731614:"Nordmänner",
587376373849522257:"Wilder Bergstamm",
587376215162355743:"Piraten",
587376337077927956:"Ägypter",
587376464815456398:"Ureinwohner",
587376621846265896:"Mystischer Orden",
587376695691051017:"Römer",
587376791170187274:"Dunkelritter",
587376876184666123:"Samurai"}

rol = {"Dunkelritter":587376791170187274,"Samurai":587376876184666123,"Römer":587376695691051017,"Mystischer Orden":587376621846265896,
"Ureinwohner":587376464815456398,"Ägypter":587376337077927956,"Piraten":587376215162355743,"Wilder Bergstamm":587376373849522257,
"Nordmänner":587376412625731614}


festungen = {"dunkelBurg":"Dunkelritter","palast":"Samurai","rom":"Römer","kirche":"Mystischer Orden","wälder das pantheon":"Ureinwohner",
"pyramide":"Ägypter","boot":"Piraten","bergfort":"Wilder Bergstamm","eiskappen":"Nordmänner"}

def log(person_name,person_id,command,channel_name,datum): #command zeigt die volle message, datum als datetime.datetime object
    global cursor
    datum = datum.split()
    tag = datum[0]
    uhrzeit = datum[1][:5]
    cursor.execute("INSERT INTO logs VALUES (?,?,?,?,?,?)",[person_name,person_id,command,channel,tag,uhrzeit])

def leiter_wechsel(fraktion,leiter_id): #Wenn sich der Leiter einer Stadt ändert
    global cursor
    cursor.execute("UPDATE fraktionen SET leiter_id = ? WHERE fraktion = ?",[leiter_id,fraktion])

def festung_einnahme(festung,fraktion): #Wenn eine Basis eingenommen wird. "fraktion" ist der neue Besitzer der Stadt
    global cursor
    cursor.execute("UPDATE festungen SET fraktion = ? WHERE festung = ?",[fraktion,festung])

def invasion_ankündigung(festung,angreifer_fraktion,verteidiger_fraktion,datum): #datum als datetime.datetime object
    global cursor
    datum = datum.split()
    tag = datum[0]
    uhrzeit = datum[1][:5]
    cursor.execute("INSERT INTO invasion VALUES (?,?,?,?,?)",[festung,angreifer_fraktion,verteidiger_fraktion,tag,uhrzeit])

def festungen():
    cursor.execute("SELECT festung FROM festungen")
    return cursor.fetchall()

async def kickcheck(fraktion):
    return 

async def giveRole(self,fraktion,payload):
        guild = self.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        await member.add_roles(discord.utils.get(guild.roles,name = fraktion),reason = "Fraktionsbeitritt",atomic=True)
        await member.remove_roles(discord.utils.get(guild.roles,name = "noch keine Fraktion"),reason = "Fraktionsbeitritt",atomic=True)
        await member.send(nachricht[fraktion])
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
            
#[<Guild id=564077511848493067 name='BT' shard_id=None chunked=True member_count=3>, <Guild id=579677389664157696 name='ðﾝﾕ﾿ðﾝﾖﾍðﾝﾖﾊ ðﾝﾕﾰðﾝﾖﾒðﾝﾖﾕðﾝﾖﾎðﾝﾖﾗðﾝﾖﾊ' shard_id=None chunked=True member_count=97>]

async def invasioncheck(self):
    guild = self.get_guild(579677389664157696)
    channel = guild.get_channel(588733944183128064)
    print(guild)
    print(channel)
    while True:
        
        f = open("invasionen.txt","r")
        rawdata = f.readlines()
        print(rawdata)
        invaNR = 0
        checkNR = 0
        for item in rawdata:
            print(item)
            invaNR += 1
        print(invaNR)
        f.close()
        while checkNR < invaNR:
            f = open("invasionen.txt","r")
            print("why")
            print(checkNR)
            satz = rawdata[checkNR]
            
            liste = satz.split(",")
            print(liste)
            print("Wtf")
            inva = liste
            print(inva)
            jahr = datetime.datetime.now().year
            tag = datetime.datetime.now().day
            monat = datetime.datetime.now().month
            stunde = datetime.datetime.now().hour
            minuten = datetime.datetime.now().minute
            
            invtag = int(inva[1])
            invmonat = int(inva[2])
            invjahr = int(inva[3])
            
            fest = inva[0]
            frak = inva[5]
            invstunde = int(inva[4])
            
            if not f.closed:
                f.close()
            
            if jahr == invjahr:
                if monat == invmonat:
                    if (invtag - tag) == 0:
                        if invstunde > stunde:
                            if invstunde-stunde == 0:
                                remainingTime = 60-minuten
                            else:
                                remainingTime = (((invstunde - stunde)*60)+(60-minuten))
                            #print(remainingTime)
                                remainingStunde = math.floor(remainingTime/60)
                            #print(remainingStunde)
                                remainingMinuten = remainingTime%60
                            #print(remainingStunde)
                            if remainingTime >= 0:
                                await channel.send("Die Fraktion " + str(festungen[fest]) + " wird in " + str(remainingStunde) + "Stunden und " +str(remainingMinuten) + "Minuten von den "+str(frak)+" angegriffen")
            checkNR += 1
        
        
        await asyncio.sleep(30)#3600
        

 


async def invasion(datum,konig,festung):
    pass
    
def archivieren(text):
    f = open("invasionen.txt","a")
    f.write(text)
    
    f.close()
    


class MyClient(discord.Client):
    async def on_member_join(self,member):
        await member.add_roles(discord.utils.get(member.guild.roles,name = "noch keine Fraktion"),reason = "Server Beitritt",atomic=True)
        await member.send("Willkommen bei The EMPRIE! Schau dir die Fraktionen in #die-fraktinoen an und wähle eine in #fraktionsbeitritt aus, um die Rolle zu erhalten!")
        
    async def on_ready(self):
        print('Logged on as', self.user)
        #await invasioncheck(self)

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
        
        if message.content.startswith("!warte"):
            await asyncio.sleep(10)
            await message.channel.send("10 Sekunden sind um")
        
        if message.content.lower() == "!fraktionsverteilung":
            global fraktionen
            rollenanzahl = {name:0 for name in fraktionen.keys()}
            
            for member in message.guild.members:
                for rolle in rollenanzahl.keys():
                    rollenanzahl[rolle] += rollencheck(rol[rolle],member)

            message = "\n".join([f"{rolle}: {rollenanzahl[rolle]}" for rolle in rollenanzahl])
            await message.channel.send(message)
            
        if message.content.startswith("!invasion"):
            if re.fullmatch("!invasion [\w\s]+, (Samstag|Sonntag) \\d\\d:\\d\\d",message.content) is None:
                print("error!") #Falscher input, error meldung im discord channel TODO
                return #keinen weiteren code ausführen

            guild = message.guild
            author = message.author
            if (await authorcheck(self,author,guild)):
                splitmsg = message.content[10:].lower().split(",")
                festung = splitmsg[0]
                if festung not in festungen.keys():
                    print("festung gibts nicht") #TODO error meldung im discord channel
                    return #keinen weiteren code ausführen
                splitmsg = splitmsg[1][1:].split(" ")
                tag = splitmsg[0]
                #uhrzeit = pyutil.timeparse(splitmsg[1]) #Whoopsie
                splitmsg = splitmsg[1].split(":")
                uhrzeit = datetime.time(int(splitmsg[0]),int(splitmsg[1]))
                nachricht = message.content[9:].lower().strip()
                fraktion = await fcheck(self,message.author,message.guild,message.author)
                nachricht= nachricht +","+str(guild.get_role(fraktion).name)+"\n"

                archivieren(nachricht)
            
            
                    
        
        
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

            if payload.message_id == fraktionen["Römer"] : #Küstenvolk/Römer
                if not (await check(self,payload)):
                   await giveRole(self,"Römer",payload)

            if payload.message_id == fraktionen["Samurai"] : #Samurai
                if not (await check(self,payload)):
                    await giveRole(self,"Samurai",payload)



client = MyClient()
client.run(TOKEN)

class Fraktion:
    def __init__(self,name,member_role,leader_role,bewerbungs_channel):
        self.name=name
        self.member_role=member_role
        self.leader_role=leader_role
        self.bewerbungs_channel=bewerbungs_channel

FRAKTIONEN = [
    Fraktion("Nordmänner",587376412625731614,587649118978179072,598904407316365325),
    Fraktion("Wilder Bergstamm",587376373849522257,587648048641867776,598903112161296394),
    Fraktion("Piraten",587376215162355743,587648225360740384,598904580067295232),
    Fraktion("Ägypter",587376337077927956,587648422761463818,598904964143906864),
    Fraktion("Ureinwohner",587376464815456398,587648931920347136,598904758065037319),
    Fraktion("Mystischer Orden",587376621846265896,587648869551308801,598904133927305216),
    Fraktion("Mongolen",587376695691051017,587648819680903171,598903651993387018),
    Fraktion("Dunkelritter",587376791170187274,587648591548383232,598903423600951336),
    Fraktion("Samurai",587376876184666123,587648705990098947,598904670999805992)
]

def get_bewerbungs_channel(fraktion_name):
    for fraktion in FRAKTIONEN:
        if fraktion.name == fraktion_name:
            return fraktion.bewerbungs_channel

def member_rolle_von_fraktion(fraktion_name):
    for fraktion in FRAKTIONEN:
        if fraktion.name == fraktion_name:
            return fraktion.member_role

def fraktion_id_von_leader_id(leader_id):
    for fraktion in FRAKTIONEN:
        if fraktion.leader_role == leader_id:
            return fraktion.member_role

def leader_rolle_von_fraktion(fraktion_name):
    for fraktion in FRAKTIONEN:
        if fraktion.name == fraktion_name:
            return fraktion.leader_role

def fraktion_von_rolle(rollen_id):
    for fraktion in FRAKTIONEN:
        if fraktion.member_role == rollen_id or fraktion.leader_role == rollen_id:
            return fraktion.name

def id_von_fraktion(rolle):
    for fraktion in FRAKTIONEN:
        if fraktion.name == rolle:
            return fraktion.member_role

def get_rollen_ids():
    return [fraktion.member_role for fraktion in FRAKTIONEN]

def alle_fraktionen():
    return [fraktion.name for fraktion in FRAKTIONEN]

def alle_member_rollen():
    return [fraktion.member_role for fraktion in FRAKTIONEN]

def alle_leader_rollen():
    return [fraktion.leader_role for fraktion in FRAKTIONEN]

def get_FRAKTIONEN():
    return FRAKTIONEN

def get_projekt_leitung_rolle():
    return [594493151234883602,596415320390893588]

def get_projekt_leitung():
    return [521087967402655767,184385677301907456,442350475950424104,235492603028570112]
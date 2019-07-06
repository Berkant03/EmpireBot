class Fraktion:
    def __init__(self,name,member_role,leader_role):
        self.name=name
        self.member_role=member_role
        self.leader_role=leader_role

FRAKTIONEN = [
    Fraktion("Nordmänner",587376412625731614,587649118978179072),
    Fraktion("Wilder Bergstamm",587376373849522257,587648048641867776),
    Fraktion("Piraten",587376215162355743,587648225360740384),
    Fraktion("Ägypter",587376337077927956,587648422761463818),
    Fraktion("Ureinwohner",587376464815456398,587648931920347136),
    Fraktion("Mystischer Orden",587376621846265896,587648869551308801),
    Fraktion("Mongolen",587376695691051017,587648819680903171),
    Fraktion("Dunkelritter",587376791170187274,587648591548383232),
    Fraktion("Samurai",587376876184666123,587648705990098947),
]


def member_rolle_von_fraktion(fraktion_name):
    for fraktion in FRAKTIONEN:
        if fraktion.name == fraktion_name:
            return fraktion.member_role

def leader_rolle_von_fraktion(fraktion_name):
    for fraktion in FRAKTIONEN:
        if fraktion.name == fraktion_name:
            return fraktion.leader_role

def fraktion_von_rolle(rollen_id):
    for fraktion in FRAKTIONEN:
        if fraktion.member_role == rollen_id or fraktion.leader_role == rollen_id:
            return fraktion.name

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

def get_projekt_leitung():
    return [521087967402655767,184385677301907456,442350475950424104,235492603028570112]
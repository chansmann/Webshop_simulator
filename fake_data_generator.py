from faker import Faker
from datetime import timedelta
from random import randint, uniform, choice
#import json

def gen_address():
    fake = Faker("de_DE")

    address_parts = fake.address().split()

    data = {
    'strasse' : address_parts[0], 
    'hausnummer': address_parts[1], 
    'plz': address_parts[2],
    'ort': address_parts[3],
    'land': 'Deutschland',
    }

    return data

def gen_customer(customer_type="C"):
    fake = Faker("de_DE")

    cust_data = {
    'telefonnummer': fake.phone_number()
    }

    if customer_type=="C":
        cust_data['unternehmen'] = " "
        cust_data['typ'] = "C"
        cust_data['vorname'] = fake.first_name()
        cust_data['nachname'] = fake.last_name()
        cust_data['email'] = fake.ascii_email()
    else:
        cust_data['unternehmen'] = fake.company()
        cust_data['kundentyp'] = "B"
        cust_data['vorname'] = fake.first_name()
        cust_data['nachname'] = fake.last_name()
        cust_data['email'] = fake.ascii_company_email()

    return cust_data

def gen_order(customer):

    fake = Faker("de_DE")

    startdate = fake.date_this_month()
    enddate = startdate + timedelta(days = randint(7,14))

    anzahl_pos = randint(1,5)

    einzelpreise = []
    pos_menge = []
    preis_ges = 0

    for i in range(anzahl_pos):
        einzelpreise.append(round(uniform(1,40),2))
        pos_menge.append(randint(1,50))
        preis_ges += einzelpreise[i] * pos_menge[i]

    order_data = {
        "kundennummer" : customer,
        "vorproduktion" : '0',
        "bestelldatum" : str(startdate),
        "enddatum" : str(enddate),
        "preis_ges" : preis_ges, #implement different prices and amount for private and business customer at a later point
        "anzahl_ges" : sum(pos_menge),
        "anmerkung" : "", #fake.paragraph(nb_sentences = 3),
        "z_auftraege" : []
    }

    for pos in range(anzahl_pos):

        r = lambda: randint(0,255)
        rand_hex_code = '#%02X%02X%02X' % (r(),r(),r())

        posnummer = pos + 1

        motive = ["Nein", "Ja"]
        motive_choice = choice(motive)
        if motive_choice == "Ja":
            motivenumber = randint(100000,999999)
        else:
            motivenumber = ''

        colors = ["Schneeweiß", "Nachtschwarz", "Wangenrot", "Giftgün", "Himmelblau", "Sonnengelb", "HSOG-Blau"]
        color_choice = choice(colors)

        pos_data = {
            "posnummer" : posnummer,
            "farbenHex" : rand_hex_code,
            "farbenbez" : color_choice,
            "artikel" : 1,
            "motiv" : motive_choice,
            "motivnummer" : motivenumber,
            "anzahl" : pos_menge[pos],
            "einzelpreis" : einzelpreise[pos]
        }
        order_data["z_auftraege"].append(pos_data)
    return order_data
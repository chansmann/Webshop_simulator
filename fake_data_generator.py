#generates random fake data for testing purpose

from faker import Faker
from random import randint, uniform, choice



def gen_address() -> dict:
    """
    generates fake adress parts and returns a dict of it
    """
    #libary to create fake data
    fake = Faker("de_DE")  

    address_parts = fake.address().split()

    #creating a dict with the generated fake data
    data = {
    'strasse' : address_parts[0], 
    'hausnummer': address_parts[1], 
    'plz': address_parts[2],
    'ort': address_parts[3],
    'land': 'Deutschland',
    }

    return data

def gen_customer(customer_type : str = "C" , adress_id : str = '') -> dict:
    """
    generates fake customer parts and returns a dict of it.
    Generated data depends on the given customer type
    """
    fake = Faker("de_DE")

    cust_data = {
        'adressID': adress_id,
        'vorname': fake.first_name(),
        'nachname': fake.last_name(),
        'telefonnummer': fake.phone_number(),
        'typ': customer_type
    }

    #check wether a business or private customer's mail and company should be generated
    if customer_type=="C":
        cust_data['unternehmen'] = " "
        cust_data['email'] = fake.ascii_email()
    else:
        cust_data['unternehmen'] = fake.company()
        cust_data['email'] = fake.ascii_company_email()

    return cust_data

def gen_order(customer : str , order_id : str , sort_value : str ) -> tuple[dict, list, list]:
    """
    Generates a fake orderhead returns a dict of it.
    Generated data depends on the given customer type
    """

    fake = Faker("de_DE")

    #generate fake date of the current month
    startdate = fake.date_this_month()

    #roll number of orderitems
    anzahl_pos = randint(1,5)

    #create variables for later return
    einzelpreise = []
    pos_menge = []
    preis_ges = 0

    #loop to create list of order line prices and quantity and calculate order value
    for i in range(anzahl_pos):
        einzelpreise.append(round(uniform(1,40),2))
        pos_menge.append(randint(1,50))
        preis_ges += einzelpreise[i] * pos_menge[i]

    order_data = {
        'bestellnummer' : order_id,
        "kundenID" : customer,
        "vorproduktion" : '0',
        "bestelldatum" : str(startdate),
        "gesamtpreis" : round(preis_ges, 2),
        "anzahl_ges" : sum(pos_menge),
        "anmerkung" : " ",
        'status_gesamt' : 'Erfasst',
        'waehrung' : '€',
        'sort' : sort_value
    }
    
    return order_data, einzelpreise, pos_menge


def gen_orderitem(order_id : str , einzelpreis : list, pos_menge : list, pos_nummer : int) -> dict:
    '''
    Generates data of a fake orderitem and returns a dict.
    '''


    #generate a random color hex
    r = lambda: randint(0,255)
    rand_hex_code = '#%02X%02X%02X' % (r(),r(),r())

    #roll wheter a orderitem with motive should be generated or not and if yes generate a random motive number
    motive = ["Nein", "Ja"]
    motive_choice = choice(motive)
    if motive_choice == "Ja":
        motivenumber = randint(100000,999999)
    else:
        motivenumber = ''

    #create the orderitem's number
    pos_bestellnummer = str(pos_nummer)+str(order_id)

    pos_data = {
        "PosBestellnummer": pos_bestellnummer,
        "bestellpositionID": pos_nummer,
        "farbenHex": rand_hex_code,
        "statusbez": "Erfasst",
        "anzahl": pos_menge,
        "motiv": motive_choice,
        "motivnummer": motivenumber,
        "einzelpreis": einzelpreis,
        "waehrung": "€",
        "bestellnummer": order_id,
        "artikelID": 1
    }
    
    return pos_data
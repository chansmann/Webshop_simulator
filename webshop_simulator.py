import requests
from random import randint, choice
import json


from fake_data_generator import gen_customer, gen_order, gen_address



URL = 'http://127.0.0.1:8000/'
API = {
    'create_customer' : 'savetokunde',
    'create_order' : 'api/createOrder',
    'all_customer' : 'api/getallCustomers',
    'create_adress' : 'rest/adress/',
    'create_customer' : 'rest/customer/'
    }

def main():

    #response = requests.post(URL + API['create_adress']+'33/', data = {'adressID' : 41})
    address_data = gen_address()
    response = requests.post(URL + API['create_address'], data = address_data)
    print(address_data)
    #response = requests.post(URL + API['create_adress'], data = address_data)
    #response = requests.delete(URL + API['create_adress']+"35/")
    #response_id = json.loads(response.text)
    #print(response_id["adressid"])

    data = {
    'album_name': 'The Grey Album',
    'artist': 'Danger Mouse',
    'tracks': [
        {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
        {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
        {'order': 3, 'title': 'Encore', 'duration': 159},
    ],
}

    customer_data = gen_customer('C')
    #customer_data['adressid'] = requests.get(URL + API['create_adress']+str(response_id["adressid"])+'/')

    response = requests.post(URL + API['create_customer'], data = customer_data)
    response_cust = json.loads(response.text)
    print(response_cust["kundenID"])

    while True:
        customer_amount = input("How many customers do you wish to create?: ")
        try:
            customer_amount = int(customer_amount)
            for customer in range(customer_amount): #create required amount of customers
                boolean = randint(0,1) #roll whether a business or a private customer should be generated
                customer += 1 #add one to customers for a proper output
                if boolean==0:
                    cust_data = gen_customer("B")
                    response = requests.post(URL + API['create_customer'], data = cust_data)
                    print("Customer "+ str(customer) + " created with response code: "+ str(response))
                else:
                    cust_data = gen_customer("C")
                    response = requests.post(URL + API['create_customer'], data = cust_data)
                    print("Customer "+ str(customer) + "created with response code: "+ str(response))
            break
        except ValueError:
            print("Please use (whole) numbers only.")

    while True:
        order_amount = input("How many orders do you wish to create (Only existing customers will be used)?: ")

        response = requests.get(URL + API['all_customer'])
        customers = json.loads(response.content)

        try:
            order_amount = int(order_amount)
            for order in range(order_amount):
                order += 1
                random_customer = choice(customers)['kundennummer']
                order_data = gen_order(random_customer)
                print(order_data)
                response = requests.post(URL + API['create_order'], data = json.dumps(order_data))
                print("Order "+ str(order) + " created with response code: "+ str(response))
            break
        except ValueError:
            print("Please use (whole) numbers only.")

    print("Job is done!")

main()








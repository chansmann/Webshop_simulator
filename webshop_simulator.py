import requests
from random import randint, choice
import json


from fake_data_generator import gen_customer, gen_order



URL = 'http://127.0.0.1:8000/'
API = {
    'create_customer' : 'savetokunde',
    'create_order' : 'api/createOrder',
    'all_customer' : 'api/getallCustomers'
}

def main():
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








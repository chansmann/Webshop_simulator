from random import choice

from fake_data_generator import gen_customer, gen_order, gen_address, gen_orderitem
from requester import post_request, next_order_get_request


"""
URL = 'http://dck02.bw.hs-offenburg.de:5000'
URL = 'http://127.0.0.1:8000/'

API = {
    'adress' : 'rest/adress/',
    'customers' : 'rest/customer/',
    'orders' : 'rest/order/',
    'order_item' : 'rest/order_item/'
    }
"""

def main():

    #response = requests.delete(URL + API['orders']+"C-14/")
    #response = requests.delete(URL + API['order_item']+"1C-14/")
    #response = requests.delete(URL + API['adress']+"42/")

    while True:
        customer_amount = input("How many customers do you wish to create?: ") #user input

        try:

            #if user dont enter an integer an exception will be raised
            customer_amount = int(customer_amount) 

            for customer in range(customer_amount): #loop to create all the customers

                #add one to customers for a proper output
                customer += 1 

                #calls a function to generate fake data and post it via the requester and stores the created and returned adress_id 
                adress_data = gen_address()
                adress_id, response = post_request('adress', 'adressid', adress_data)

                #rolls if business or pirvate customer should be created
                cust_types = ['C', 'B']
                customer_type = choice(cust_types)

                #calls a function to generate fake data and post it via the requester and stores the created and returned customer_id 
                cust_data = gen_customer(customer_type, adress_id)
                customer_id, response = post_request('customer', 'kundenID', cust_data)

                #performs an output with the created customer, adress id and response code
                print("Customer "+ str(customer_id) + " created with adressID: " + str(adress_id) + " and response code: "+ str(response))

                #calls a function to get the next order id (depending on customer type) and sorting value
                next_business_order, next_non_business_order, next_sort_value = next_order_get_request()
                if customer_type == 'C':
                    order_id = next_non_business_order
                else:
                    order_id = next_business_order

                #calls a function to generate a random order head and post it via the requester and stores the created and returned orderID, the over all value and amount
                order_data, einzelpreise, pos_mengen = gen_order(customer_id, order_id, next_sort_value)
                order_id, response = post_request('order', 'bestellnummer', order_data)

                #performs an output with the created Order and response code
                print("Order "+ str(order_id) + " created with response code: "+ str(response))

                #loop to generate order items depending on the returned item price/amount lists
                for pos_nummer, (einzelpreis, pos_menge) in enumerate(zip(einzelpreise, pos_mengen), start = 1):

                    #calls a function to generate random order item data and post it via the requester and stores the created and returned orderItemID 
                    order_item_data = gen_orderitem(order_id, einzelpreis, pos_menge, pos_nummer)
                    order_item_id, response = post_request('order_item', 'PosBestellnummer', order_item_data)

                    #performs an output with the created orderItem and response code
                    print("Orderitem "+ str(order_item_id) + " created with response code: "+ str(response))

            print("Job is done! " + customer + " new Entrees created!")

        except ValueError:
            print("Please use (whole) numbers only.")

main()









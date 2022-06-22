#functions to perform post and get requests

import requests
import json

URL = 'http://dck02.bw.hs-offenburg.de:5000'
URL = 'http://127.0.0.1:8000/'

API = {
    'adress' : 'rest/adress/',
    'customer' : 'rest/customer/',
    'order' : 'rest/order/',
    'order_item' : 'rest/order_item/'
    }


def post_request(api_endpoint : str, primary_key : str, dataload : dict) -> tuple[str, object]:
    '''
    Make a post request to the hs server with given dataload, api endpoint and desired primary key.
    Returns primary key of the created data and the hole response object
    '''

    #post request and store the response
    response = requests.post(URL + API[api_endpoint], data = dataload)

    #Extract the primary key from the response
    response_dict = json.loads(response.text)
    post_response_id = response_dict[primary_key]

    return post_response_id, response

def next_order_get_request() -> tuple[str, str, str]:

    '''
    Make a get request to the hs server's order rest api.
    To find out what ordernumber of private and business customer comes next.
    Returns order number of next business and non business (private) order and the next sorting value
    '''

    #get request to get all existing orderheads
    response = requests.get(URL + API['order'])

    #extract the orderlist of the response
    order_list = json.loads(response.text)

    #dictionary to store lists with ordernumbers
    order_attributes = {
        "business_orderids" : [],
        "non_business_orderids" : [],
        "sort_value_list" : []
    }

    #list to store all last or highest values of the order attributes dict
    last_order_variables = []

    #loops over all orders and append the value to the attribute dict
    for order in order_list:

        if order['bestellnummer'][0] == 'C':
            order_attributes['non_business_orderids'].append(int(order['bestellnummer'][2:])) #takes only the last to digits of an order number
        else:
            order_attributes['business_orderids'].append(int(order['bestellnummer'][2:]))

        order_attributes['sort_value_list'].append(order['sort'])

    #loop over all lists in the dict, sort it and append the last number to the result list
    for key in order_attributes:

        last_value = highest_list_value(order_attributes[key])
        last_order_variables.append(last_value)

    #generate the next numbers of orders and sorting values
    next_business_order = 'B-'+str(last_order_variables[0] + 1)
    next_non_business_order = 'C-'+str(last_order_variables[1] + 1)
    next_sort_value = last_order_variables[2] + 1

    return next_business_order, next_non_business_order, next_sort_value

def highest_list_value(list : list) -> int:
    '''
    Sort a given list and gives back its last entree
    '''
    if len(list) == 0:
        last_value = 0
    else:
        list.sort()
        last_value = list[-1]
    return last_value
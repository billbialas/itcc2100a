###############################################################################################
#   ITCC2100
#   Python API Functions program
#   
#   Author:     Bill Bialas
#   Created:    02/18/2023
#   Updated:    
#
#   Description: Program to demonstrate using the requests module to make calls to an API
#
#   Files:      api_example.py -   Main python script
#
#   API Service: https://jsonplaceholder.typicode.com/
#
################################################################################################

import os, sys
import requests
import pprint
import logging

# Setup some logging output
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
# Function for the API get
# No return here
def invoke_http_get(url:str):
    logger.info("API function- http get")

    response = requests.get(url)    # Make the request

    if not response.ok:             # Check if OK, No? Then throw error
        raise Exception('API call error')
    
    # Iterate over json data and display the results
    for data in response.json():
        print (f"{data['postId']} {data['name']}  {data['email']}  {data['body']}\n")

# Function for the API Post
# Using my user-id json data from week5
def invoke_http_post (url:str):
    logger.info("API function- http post")
    
    json_data = {
                "pk": "p40219",
                "sk": "Doctor",
                "Title": "Doctor",
                "First_Name": "John",
                "Last_Name":  "Smith",
                "Department": "Radiology",
                "Phone_1": "555-555-5555",
                "Phone_2": "555-555-3434",
                "Email": "johnsmith@gmail.com",
                "DOB": "1968-04-24",
                "Address_1":"123 Big Road",
                "Address_2":"",
                "City":"Detroit",
                "State":"MI",
                "Zip":"45874"
            }
    
    response = requests.post(url,data=json_data)    # Make request
    
    if not response.ok:             # Check if OK, No? Then throw error
        raise Exception('API call error')
    
    json_data = response.json()
    
    # Use pretty print to make output more readable
    pp= pprint.PrettyPrinter(indent=5)
    print("\nJSON Output")
    pp.pprint(json_data)

    # Another way to view the output
    print("\nAnother view of some of the data")
    print(f"{json_data['id']}  |  {json_data['First_Name']} {json_data['Last_Name']}  |  {json_data['Email']}\n")

def main ():
    logger.info("API functions script start")
 
    url_root = 'https://jsonplaceholder.typicode.com'   # Set root api url

    # Make API calls    
    invoke_http_get(url=f"{url_root}/comments")     # Use sample comments json data
    invoke_http_post(url=f"{url_root}/posts")       # Use my data

    logger.info("API functions script end")

if __name__ == '__main__':
    main()



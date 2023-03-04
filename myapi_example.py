###############################################################################################
#   ITCC2100
#   Python API Functions program
#   
#   Author:     Bill Bialas
#   Created:    02/18/2023
#   Updated:    
#
#   Description: Program to demonstrate using the requests module to make a call to my api function
#
#   Files:      myapi_example.py -   Main python script
#
#   API Service: https://3c2v2jf4zl.execute-api.us-east-1.amazonaws.com   < From the lab-learner project
#
################################################################################################

import os, sys
import requests
import logging

# Setup some logging output
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
API_JSON_DATA = None

# Function for the API get
# No return here
def invoke_my_function(url:str)->bool:
    logger.info("API function- http get")

    global API_JSON_DATA    # Use global var for user info in main function

    response = requests.get(url)    # Make the request

    # Validate status code- Requirements call for 200 as only valid response
    if response.status_code == 200:
        API_JSON_DATA = response.json()
        return True
    else:    
        return False
      
def main ():
    logger.info("API functions script start")
 
    url_root = 'https://3c2v2jf4zl.execute-api.us-east-1.amazonaws.com'   # Set root api url

    # Make API calls    
    if invoke_my_function(url=f"{url_root}/my-function"):     # Call my function
        print (f"API response is valid (=200).  Response json = {API_JSON_DATA}")
    else:
        print ("API response is not valid (!=200). Response json = Nothing")
        
    logger.info("API functions script end")

if __name__ == '__main__':
    main()



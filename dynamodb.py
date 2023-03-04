###############################################################################################
#   ITCC2100
#   Python AWS DynamoDB Functions program
#   
#   Author:     Bill Bialas
#   Created:    02/05/2023
#   Updated:    
#   
#
#   Description: Program will display a console menu of several choices
#                   to demonstrate the usage of AWS boto3 api for DynamoDB
#
#   Files:      dynamodb.py -   Main python script
#
#   Knowns:     Not all error trapping has been completed due to time constraints.
#               However, all functionality per requirements has been unit tested
#
################################################################################################

import sys
import boto3
from botocore.exceptions import ClientError
import pprint

docker = True

# Instantiate Dynamo client and resource
if docker:
    DDB_CLIENT = boto3.client('dynamodb', 
                        endpoint_url = 'http://localhost:8000', 
                        region_name = 'dummy',
                        aws_access_key_id = 'dummy',
                        aws_secret_access_key='dummy')
    DDB_RESOURCE = boto3.resource('dynamodb', 
                        endpoint_url = 'http://localhost:8000', 
                        region_name = 'dummy',
                        aws_access_key_id = 'dummy',
                        aws_secret_access_key='dummy')
else:
    DDB_CLIENT = boto3.client('dynamodb', region_name = 'us-east-1')
    DDB_RESOURCE = boto3.resource('dynamodb', region_name='us-east-1')

# Data to be loaded into DB - Python List of Lists
PRODUCT_LIST = [['Mustang','Car', '50.00'],['Corvette','Car', '100.00'], 
                ['Charger','Car', '150.00'],['Car','Mustang', '50.00'],['Car','Corvette', '100.00'], 
                ['Car','Charger', '150.00'],['Truck','F150', '250.00'],['Truck','Ram', '350.00'],
                ['Truck','Sonoma', '450.00'],['F150','Truck', '250.00'],['Ram','Truck', '350.00'],
                ['Sonoma','Truck', '450.00']] 

# Create table function
def create_table():
   
    def load_data():    # Used to load data and called further down in create_table function
        
        print ("Loading data\n")

        for item in PRODUCT_LIST:
            try:
                response = DDB_CLIENT.put_item(
                        TableName=table_name,
                        Item={
                            'product_name': {
                                'S': item[0]
                            },
                            'product_key': {
                                'S': item[1]
                            },
                            'product_price':{
                                'N': item[2] #number passed in as a string (ie in quotes)
                            }
                        },
                        #ConditionExpression='attribute_not_exists(product_name)'
                    )
        
            except ClientError as e:
                raise
        
        print ("Data load completed")

    table_name = input ("Please enter table name? ")    # Prompt for table name

    # define parms needed to create table
    params = {
        'TableName':table_name,
        'KeySchema':[
            {
                'AttributeName': 'product_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'product_key',
                'KeyType': 'RANGE'
            }
        ],
        'AttributeDefinitions':[
            {
                'AttributeName': 'product_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'product_key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'product_price',
                'AttributeType': 'N'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        'GlobalSecondaryIndexes':[
            {
            'IndexName': 'product-id-idx',
            'KeySchema': [
                {
                    'AttributeName': 'product_key',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'product_name',
                    'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
                },
            'ProvisionedThroughput' : {
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
            },
             {
            'IndexName': 'price-id-idx',
            'KeySchema': [
                {
                    'AttributeName': 'product_key',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'product_price',
                    'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
                },
            'ProvisionedThroughput' : {
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
            }
        ]
    }

    print (f"Creating table: {table_name}")
    
    table = DDB_CLIENT.create_table(**params)           # Create table via API
    waiter = DDB_CLIENT.get_waiter('table_exists')      # Wait for table to be created
    waiter.wait(TableName=table_name)
    
    print (f"Table: {table_name} created.")

    load_data()     # Load some data

    return input ("\nPress enter to continue...")

# List tables function
def list_tables():

    print ("Listing current DynamoDB tables\n")
    
    try:
        response = DDB_CLIENT.list_tables()
       
        if response.get('TableNames'):
            for table in response.get('TableNames'):
                print(table)
        else:
            print ("Nothing to display")
    
    except ClientError as e:
        print (f"Error: {e}")
        raise
    
# Get table details function
# Ran out of time for this to display pretty, just shows standard AWS return
def table_details():

    table_name = input ("Please enter table name? ") 

    response = DDB_CLIENT.describe_table(TableName=table_name)

    # Try to make a bit nicer
    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(response)

    return input ("\nPress enter to continue...")

# List items function
def list_items(table_name):

    # Get Items for user to see 
    print (f"Displaying current items for table: {table_name}")
    
    tbl_items = DDB_RESOURCE.Table(table_name).scan()
    
    print ("\n{:20}{:15}".format("Product Name","Product Key"))
    
    # Iterate the list and display the items 
    for item in tbl_items['Items']:
        print(f"{item.get('product_name'):20}{item.get('product_key'):15}")
    
    print("")

# Get item function
# No very good validation for user inputs
def get_item():
    
    table_name = input ("Please enter table name? ") 
    list_items(table_name)  # List items so user has an idea of whats in table

    p_key = input ("Please enter product name? ") 
    s_key = input ("Please enter product key? ") 

    try:
        response = DDB_CLIENT.get_item(
            Key={
                'product_name': {
                    'S': p_key,
                },
                'product_key': {
                    'S': s_key,
                },
            },
            TableName=table_name,
        )
       
        # Check if there is something returned and the display it with the additional attribute
        if 'Item' in response: 
            price = response.get('Item').get('product_price').get('N')  
            print ("\n{:20}{:15}{:10}".format("Product Name","Product Key","Price"))
            print(f"{p_key:20}{s_key:15}{price:10}")
        else:
            print ("Key(s) not found")
    
    except ClientError as e:
        print (f"Error: {e}")
        raise

    return input ("\nPress enter to continue...")

# Delete item function
def delete_item():
    table_name = input ("Please enter table name? ") 
    list_items(table_name)  # List items to make easier for user
    
    p_key = input ("Please enter product name? ") 
    s_key = input ("Please enter product key? ") 

    try:
        response = DDB_CLIENT.delete_item(
            Key={
                'product_name': {
                    'S': p_key,
                },
                'product_key': {
                    'S': s_key,
                },  
            },
            TableName=table_name,
        )
    
        print("Item deleted.\n")    # Not sure if there is a waiter for item delete but appears to be fast

        list_items(table_name)  # List items to show it is now gone
        
        return input ("\nPress enter to continue...")

    except ClientError as e:
        print (f"Error: {e}")
        raise

# Delete table function
def delete_table():    

    list_tables()       # show user tables to make easier

    table_name = input ("Please enter table name? ") 
    
    try:
        response = DDB_CLIENT.delete_table(         # Delete table
            TableName=table_name
        )

        print (f"Deleting table: {table_name}")

        waiter = DDB_CLIENT.get_waiter('table_not_exists')  # 
        waiter.wait(TableName=table_name)                   # Wait for it to be deleted before moving on 
        print (f"Table: {table_name} deleted.")

        list_tables()

    except ClientError as e:
        print (f"Error: {e}")
        raise
  
    return input ("\nPress enter to continue...")

# Query table
# Again ugly output for lack of time
def query_table():

    list_tables()

    table_name = input ("Please enter table name? ") 
    p_key = input ("Please enter product name? ") 
    
    tbl_items = DDB_CLIENT.query(
        ExpressionAttributeValues={
            ':v1': {
                'S': p_key,
            },
        },
        KeyConditionExpression='product_name = :v1',
        TableName=table_name,
    )

    print ("Query results.")
    for item in tbl_items['Items']:
        print (item)
   
# Main
def main():
   
    exit = False        # Used to exit menu

    while not exit:
        print ("\nWelcome to AWS DynamoDB Example\n")
        print ("1- Create Table & Load Sample Data") 
        print ("2- Show Tables") 
        print ("3- Show Table Details")         
        print ("4- Get Item") 
        print ("5- Delete Item") 
        print ("6- Delete Table")
        print ("7- Query by Range") 
        print ("E- Exit")
        action = input("Please choose an option: ")

        if action.lower() =='e':
            print ("Exiting..")
            exit = True
        elif action =='1':
            create_table()
        elif action =='2':
            list_tables()
        elif action =='3':
            table_details()
        elif action =='4':
            get_item()
        elif action =='5':
            delete_item()
        elif action =='6':
            delete_table()
        elif action == '7':
            query_table()

if __name__ == '__main__':
    main()
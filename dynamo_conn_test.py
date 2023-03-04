
import sys
import boto3
from botocore.exceptions import ClientError
import pprint

DDB_CLIENT = boto3.client('dynamodb', 
                        endpoint_url = 'http://localhost:8000', 
                        region_name = 'dummy',
                        aws_access_key_id = 'dummy',
                        aws_secret_access_key='dummy')
        
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
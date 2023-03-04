###############################################################################################
#   ITCC2100
#   Python AWS Lambda Proggram
#   
#   Author:     Bill Bialas
#   Created:    02/24/2023
#   Updated:    
#   
#
#   Description: This program will run some code as a Lambda in AWS
#
#   Files:      lambda_example.py -   Main python script
#
#   Knowns:     Not all error trapping has been completed due to time constraints.
#               However, all functionality per requirements has been unit tested
#
################################################################################################

import sys
import boto3
from botocore.client import ClientError
import logging

# Setup Logger for output
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Instantiate s3 client and resource
s3client = boto3.client('s3')

bucket_name = 'itcc2100bialastest'      # Bucket name for testing

# Function to create the bucket
def create_bucket():

    try:
        logger.info(f"Creating bucket: {bucket_name}")
        response = s3client.create_bucket(Bucket=bucket_name)
   
    except ClientError as e:
        logging.error(e)

# Function to write some files
def write_to_bucket():

    logger.info(f"Writing files to bucket: {bucket_name}")

    # Files to upload- List
    object_keys = ['sample_file.txt','sample_file_1.txt','sample_file_2.txt']

    try:
        # Iterate the file list an upload
        for object_key in object_keys:
            logger.info(f'Uploading some data to {bucket_name} with key: {object_key}')
            body = f"Hello World! from file: {object_key}".encode('utf-8')  # Convert string to bytes
            s3client.put_object(Bucket=bucket_name, Key=object_key, Body=body)
      
    except ClientError as e:
        logging.error(e)

# Function to list files in the bucket
def list_bucket_files():
    
    logger.info(f"Listing files in bucket: {bucket_name}")
    
    try:
        response = s3client.list_objects(Bucket=bucket_name)
        
        if 'Contents' in response:  # Validate there is an object in the bucket
            # Iterate objects and display metadata
            for object in response['Contents']:
                logger.info (f"Object Name: {object['Key']} | Last Mod Date: {object['LastModified']} | StorageClass: {object['StorageClass']}")
        else:
            logger.info  ("No objects to list")

    except ClientError as e:
        logging.error(e)
   
# Main entry point   
def lambda_handler(event, context):
    
    # Call the functions to make the fun happen!
    try:
        logger.info(f"Lambda function running")
        create_bucket()
        write_to_bucket()
        list_bucket_files()
        return {"statusCode": 200, "body": "Lambda function success!"}
    
    except ClientError as e:
        logger.info(f"Error listing buckets: {e}")
        return {"statusCode": 400, "body": "Lambda function fail!"}

# Dev use only
if __name__ == '__main__':
    lambda_handler(None, None)
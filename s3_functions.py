###############################################################################################
#   ITCC2100
#   Python AWS S3 Functions program
#   
#   Author:     Bill Bialas
#   Created:    01/22/2023
#   Updated:    
#   
#
#   Description: Program will display a console menu of several choices
#                   to demonstrate the usage of AWS boto3 api
#
#   Files:      s3_functions.py -   Main python script
#               sample_file.txt, sample_file_1.txt, sample_file_2.txt- used for uploading
#
#   Knowns:     Not all error trapping has been completed due to time constraints.
#               However, all functionality per requirements has been unit tested
#
################################################################################################

import sys
import boto3
from botocore.client import ClientError

# Instantiate s3 client and resource
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

# Get user input for bucket name when needed or continue with program code
def get_usr_input(action=None):

    if action=='continue':
        return input ("\nPress enter to continue...")
    else:
        return input ("Please enter bucket name? ")
        
# Check if bucket name is valid/exists
def valid_bucket(bucket_name):
    
    get_bucket= s3resource.Bucket(bucket_name)

    try:
        s3resource.meta.client.head_bucket(Bucket=get_bucket.name)  # Use resource instead of client this time
        return True
    
    except ClientError as e:
        print (f"Bucket <{bucket_name}> does not exist or you have no access")
        return False

# Check if the object exists in the bucket
def valid_object(bucket_name, object_name):

    try:
        response = s3client.get_object(Bucket=bucket_name,Key=object_name)
        return True     # No error indicates something is there
    
    except ClientError as e:
        print (f"Object <{object_name}> does not exist or you have no access")
        return False

# Create bucket function
def create_bucket():
    bucket_name = get_usr_input()     # get user input for bucket name

    if bucket_name:
        try:
            print(f'Creating new bucket with name: {bucket_name}')
            response = s3client.create_bucket(Bucket=bucket_name)
            get_usr_input('continue')

        except ClientError as e:
            print (f"Error creating bucket: {e}")
            sys.exit(1)
    else:
        print ("Invalid name please try again")

# Delete bucket function
def delete_bucket():
    bucket_name = get_usr_input()     # get user input for bucket name
   
    if valid_bucket(bucket_name):   # Check if bucket is valid
        try:
            print(f'Deleting bucket with name: {bucket_name}')
            response = s3client.delete_bucket(Bucket=bucket_name)
            get_usr_input('continue')

        except Exception as e:
            print (f"Error deleting bucket: {e}")
            sys.exit(1)
    else:
        print ("Please try again")
        
# List all buckets function
def list_buckets():
    print ("List Buckets")

    try:
        print(f'Listing all buckets:')
        response = s3client.list_buckets()

        # Iterate through response on keyword Buckets
        for bucket in response['Buckets']:
            print (f"Bucket Name: {bucket['Name']} | Bucket Created: {bucket['CreationDate']}")
        get_usr_input('continue')
    
    except ClientError as e:
        print (f"Error listing buckets: {e}")
        sys.exit(1)
    
# Upload file(s) t0 bucket function
def upload_file():
    print ("Upload file(s) to bucket")
 
    # Files to upload- List
    object_keys = ['sample_file.txt','sample_file_1.txt','sample_file_2.txt']

    bucket_name = get_usr_input()     # get user input for bucket name
   
    if valid_bucket(bucket_name):   # Check if bucket is valid
        try:
            # Iterate the file list an upload
            for object_key in object_keys:
                print(f'Uploading some data to {bucket_name} with key: {object_key}')
                body = f"Hello World! from file: {object_key}".encode('utf-8')  # Convert string to bytes
                s3client.put_object(Bucket=bucket_name, Key=object_key, Body=body)
            get_usr_input('continue')

        except ClientError as e:
            print (f"Error listing buckets: {e}")
            sys.exit(1)
    else:
        print ("Please try again")
        
# List objects in bucket
def list_bucket_files():
    print ("list files (objects) in a bucket")
 
    bucket_name = get_usr_input()     # get user input for bucket name

    if valid_bucket(bucket_name):   # Check if bucket is valid
        try:
            response = s3client.list_objects(Bucket=bucket_name)
            
            if 'Contents' in response:  # Validate there is an object in the bucket
                # Iterate objects and display metadata
                for object in response['Contents']:
                    print (f"Object Name: {object['Key']} | Last Mod Date: {object['LastModified']} | StorageClass: {object['StorageClass']}")
                get_usr_input('continue')
            else:
                print ("No objects to list")
                get_usr_input('continue')

        except ClientError as e:
            print (f"Error listing objects: {e}")
            sys.exit(1)
    
# Delete bucket files
# User inputs bucket name and object name
def delete_bucket_files():
    print ("delete file (objects) in a bucket")
 
    bucket_name = get_usr_input()     # get user input for bucket name
    object_name = input ("Enter file/object name? ")

    if valid_bucket(bucket_name):   # Check if bucket is valid
        if valid_object(bucket_name=bucket_name, object_name=object_name):      # Check if object is valid
            try:
                response = s3client.delete_object(Bucket=bucket_name,Key=object_name)
                get_usr_input('continue')

            except ClientError as e:
                print (f"Error deleting object: {e}")
                sys.exit(1)
        else:
            print ("Please try again")
    else:
        print ("Please try again")
        
# List contents of an object in a bucket
# User inputs bucket name and object name
def list_object_contents():
    bucket_name = get_usr_input()     # get user input for bucket name
    object_name = input ("Enter file/object name? ")
    
    if valid_bucket(bucket_name):   # Check if bucket is valid
        if valid_object(bucket_name=bucket_name, object_name=object_name):  # Check if object is valid
    
            response = s3client.list_objects(Bucket = bucket_name, Prefix=object_name)
            
            try:
                for object in response.get('Contents'):
                    data = s3client.get_object(Bucket=bucket_name, Key=object.get('Key'))
                    contents = data['Body'].read()
                    print("\n-------------------------------------------------")
                    print(contents.decode("utf-8"))     # From bytes to string
                    print("---------------------------------------------------")
                  
            except ClientError as e:
                    print (f"Error listing objects: {e}")
                    sys.exit(1)
# Main
def main():
    exit = False        # Used to exit menu
    while not exit:
        print ("\nWelcome to AWS S3 Example\n")
        print ("1- Create a bucket") 
        print ("2- List all buckets") 
        print ("3- Upload a file") 
        print ("4- List all files in a particular bucket")
        print ("5- Delete a file") 
        print ("6- Delete a bucket") 
        print ("7- List File Contents") 
        print ("E- Exit")
        action = input("Please choose an option: ")

        if action.lower() =='e':
            print ("Exiting..")
            exit = True
        elif action =='1':
            create_bucket()
        elif action =='2':
            list_buckets()
        elif action =='3':
            upload_file()
        elif action =='4':
            list_bucket_files()
        elif action =='5':
            delete_bucket_files()
        elif action =='6':
            delete_bucket()
        elif action == '7':
            list_object_contents()

if __name__ == '__main__':
    main()
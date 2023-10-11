import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get keys, bucket name, editor flag, and endpoint_url from environment variables
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
bucket_name = os.getenv('BUCKET_NAME')
editor = os.getenv('EDITOR')
endpoint_url = os.getenv('ENDPOINT_URL')

# Error handling for missing environment variables
if not access_key or not secret_key or not bucket_name or not endpoint_url:
    raise ValueError("Missing necessary environment variables - check your .env file")

session = boto3.session.Session()

s3 = session.client(
    service_name='s3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=endpoint_url,
)

# List Objects in the Bucket
try:
    objects = s3.list_objects(Bucket=bucket_name)
    print(f"Objects in {bucket_name}:")
    for obj in objects.get('Contents', []):
        print(obj['Key'])
except Exception as e:
    print(f"Error accessing {bucket_name}: {str(e)}")

# If editor is 'true', Create and then Delete a test.txt file in the Bucket
if editor == 'true':
    # Create a test.txt file in the Bucket
    try:
        s3.put_object(Bucket=bucket_name, Key='test.txt', Body='This is a test file')
        print('Successfully created test.txt in the bucket.')
    except Exception as e:
        print(f"Error creating test.txt in {bucket_name}: {str(e)}")

    # Delete the test.txt file from the Bucket
    try:
        s3.delete_object(Bucket=bucket_name, Key='test.txt')
        print('Successfully deleted test.txt from the bucket.')
    except Exception as e:
        print(f"Error deleting test.txt from {bucket_name}: {str(e)}")

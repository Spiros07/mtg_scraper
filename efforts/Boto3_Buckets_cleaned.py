import boto3
import logging
import os
from botocore.exceptions import ClientError

def show_all_buckets():
    s3_l = boto3.resource('s3')
    for bucket in s3_l.buckets.all():
        print(bucket.name)
show_all_buckets()

s3.create_bucket(Bucket="aicorepythontest")
show_all_buckets()


s3 = boto3.client('s3')

s3.delete_bucket(Bucket="aicorepythontest")
show_all_buckets()

def show_all_buckets_and_contents():
    s3_l = boto3.resource('s3')
    for bucket in s3_l.buckets.all():
        print(f"BUCKET: {bucket.name}")
    
    for obj in bucket.objects.all():
        print(obj.key)
    
show_all_buckets_and_contents()



def upload_file(file_name, bucket="", object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


s3 = boto3.client('s3')



with open("index.html", "rb") as f:
    s3.upload_fileobj(f, "aicoretest", "python_index.html")

show_all_buckets_and_contents()


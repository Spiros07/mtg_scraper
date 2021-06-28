from botocore.exceptions import ClientError
import logging
import boto3
import botocore


BUCKET = ''

def download_file(file_name, bucket, object_name=None):
    """
    Downloads a file from an S3 bucket
    
    Parameters
    ----------
    file_name : str
        Name of the file we want to download.
    bucket: str
        Name of the bucket
    object_name:
        Name we want to give to the file once stored in our machine

    Returns
    -------
    bool
        False if the upload caused an error. True if the upload was successful
    """
    if object_name is None:
        object_name = file_name
        
    s3 = boto3.client('s3')

    try:
        s3.download_fileobj(bucket, file_name, object_name)

    # The file might be corrupted, or might have disappear (which would be strange)
    # so we can catch the error using the try, except error handling

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise



def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket
    
    Parameters
    ----------
    file_name : str
        Name of the file we want to upload
    bucket: str
        Name of the bucket
    object_name:
        Name of the object as we want it to appear in the bucket

    Returns
    -------
    bool
        False if the upload caused an error. True if the upload was successful
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
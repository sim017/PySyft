"""Setup Instructions

# Setups 4 server nodes with two drives with a nginx layer
docker compose -f docker-compose-minio.yml up


# pip install minio
# pip install boto3

# By default versioning of objects is off
# Versioning allows to keep multiple versions of the same object under the same key.

AdminPage: "http://localhost:9000"
Username: minio
Password: minio123
"""

# stdlib
from io import BytesIO

# third party
import boto3
from botocore.client import Config
import requests

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ROOT_USER = "minio"
MINIO_ROOT_PWD = "minio123"
bucket_name = "mybucket"


def get_client():
    client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ROOT_USER,
        aws_secret_access_key=MINIO_ROOT_PWD,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    return client


s3_client = get_client()


def create_bucket():
    resp = s3_client.list_buckets()
    bucket_exists = any([bucket["Name"] == bucket_name for bucket in resp["Buckets"]])
    if not bucket_exists:  # bucket already created
        print("Creating Bucket.....")
        resp = s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket created: ", resp)
    else:
        print("Bucket Already Exists !!!")

    resp = s3_client.list_buckets()
    print("-------------List available buckets------------\n")
    print(resp)
    print("-----------------------------------------------")


def upload_files():
    """Uploading files to S3"""

    print("Uploading binary data....")
    data = BytesIO(bytes(1024**3))  # 1GB data
    object_key = "fileupload/1GBdata.bin"  # `fileupload` is the folder inside which this file will be stored
    print(f"Key: {object_key}")
    s3_client.upload_fileobj(Fileobj=data, Bucket=bucket_name, Key=object_key)

    # Check if the object is uploaded correctly
    print("--------Uploaded Objects-----------")
    print(s3_client.list_objects(Bucket=bucket_name).get("Contents", []))
    print("-----------------------------------------------\n")

    # Generating a pre-signed url to get the uploaded object
    print("Creating presigned get url..........")
    get_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=300,  # expiration time of the url in seconds
        HttpMethod="GET",
    )
    print("Presigned Get Url: ", get_url)
    print()

    # Uploading file using pre-signed PUT url
    print("Creating presigned PUT url..........")
    object_key = "bindata/binObjectPUT.bin"  # Storing it in another folder `bindata`
    response = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=300,
        HttpMethod="PUT",
    )
    data = bytes(1024**3)  # 1GB data
    files = {"file": (object_key, data)}
    print("Uploading object using PUT presigned url..........")
    print(f"Key: {object_key}")
    http_response = requests.put(response, files=files)  # Creating a PUT
    print(http_response.status_code)  # Check status of the response, should return 200
    assert http_response.status_code == 200

    # Check if the object was uploaded
    print("--------Uploaded Objects-----------")
    print(s3_client.list_objects(Bucket=bucket_name).get("Contents", []))
    print("-----------------------------------------------\n")

    # Uploading file using pre-signed POST url
    print("Creating POST presigned url..........")
    object_key = "bindata/binObject1GBPost.bin"
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=object_key,
        ExpiresIn=3600,
    )
    data = bytes(1024**3)  # 1GB data
    files = {"file": (object_key, data)}
    print("Uploading object using POST presigned url..........")
    print(f"Key: {object_key}")
    http_response = requests.post(response["url"], data=response["fields"], files=files)
    print(http_response.status_code)  # Check status of the response, should return 204
    assert http_response.status_code == 204

    # Check if the object was uploaded
    print("--------Uploaded Objects-----------")
    print(s3_client.list_objects(Bucket=bucket_name).get("Contents", []))
    print("-----------------------------------------------\n")

    # Uploading file using pre-signed POST url but with limits on the file
    object_key = "bindata/binObject500MBLimitPost.bin"
    min_file_size = 0  # 0 Mb
    max_file_size = 500 * 1024**2  # 500 Mb

    conditions = [["content-length-range", min_file_size, max_file_size]]
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=object_key,
        ExpiresIn=3600,
        Conditions=conditions,
    )
    files = {"file": (object_key, data)}
    print(
        "Uploading file using pre-signed POST url but with object size greater than given limit"
    )
    print(f"Key: {object_key}")
    http_response = requests.post(
        response["url"], data=response["fields"], files=files
    )  # Creating a POST request
    print("Uploading 1Gb file where allowed limit is 500Mb")
    print(
        http_response.status_code
    )  # This should fail, as the data exceeds given limit.
    assert http_response.status_code == 400

    print("Uploading 400Mb file where allowed limit is 500Mb")
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=object_key,
        ExpiresIn=3600,
        Conditions=conditions,
    )
    data = bytes(400 * 1024**2)  # 1GB data
    files = {"file": (object_key, data)}
    print(
        "Uploading file using pre-signed POST url but with object size less than given limit"
    )
    print(f"Key: {object_key}")
    http_response = requests.post(
        response["url"], data=response["fields"], files=files
    )  # Creating a POST request
    print(
        http_response.status_code
    )  # This should fail, as the data exceeds given limit.
    assert http_response.status_code == 204

    # Check if the object was uploaded
    print("--------Uploaded Objects-----------")
    print(s3_client.list_objects(Bucket=bucket_name).get("Contents", []))
    print("-----------------------------------------------\n")


if __name__ == "__main__":
    # Create bucket
    create_bucket()

    # Upload file
    upload_files()

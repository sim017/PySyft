"""Setup Instructions


# Setup master
docker run -p 9333:9333 -p 19333:19333 --name master chrislusf/seaweedfs master

# Setup volume
docker run -it -p 8080:8080 -v `pwd`/swfs_data:/data --name volume --link master chrislusf/seaweedfs volume -max=10 -mserver="master:9333" -port=8080 -publicUrl="127.0.0.1:8080"

# Setup filer
docker run -it -p 8888:8888 -v `pwd`/filer_data:/data --name filer --link master chrislusf/seaweedfs filer -master="master:9333"

# Setup s3
docker run -it -p 8333:8333 -v `pwd`/filer_data:/data --name s3 --link filer chrislusf/seaweedfs s3 -filer="filer:8888" -config=s3config.json


# For s3 access enpoint configuration refer to filer_data/s3config.json

# Install packages
pip install python-weed
pip install boto3
"""

# third party
import boto3
import requests

S3_ENDPOINT = "http://localhost:8333"


def get_client():
    # For reference: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    config = boto3.session.Config(signature_version="s3v4")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id="admin",  # Defined in filer_data/s3config.json
        aws_secret_access_key="admin",  # Defined in filer_data/s3config.json
        region_name="us-east-1",  # could be anything region locally
        config=config,
        endpoint_url=S3_ENDPOINT,
    )
    return s3_client


s3_client = get_client()
bucket_name = "myBucket"


def create_bucket():
    resp = s3_client.list_buckets()
    bucket_exists = any([bucket["Name"] == bucket_name for bucket in resp["Buckets"]])
    if not bucket_exists:  # bucket already created
        resp = s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket created: ", resp)

    resp = s3_client.list_buckets()
    print("Listing available buckets:", resp)


def upload_file():

    print("Uploading file using filepath")
    # Uploading file using filepath
    filename = "profile2.html"  # path of the file on your local system
    object_key = "profile.html"  # path or name of the file on s3
    s3_client.upload_file(Filename=filename, Bucket=bucket_name, Key=object_key)

    print("Uploading file as object")
    # Uploading file or binary object
    object_key = "profileasbinary.html"  # path or name of the file on s3
    with open("profile2.html", "rb") as f:
        s3_client.upload_fileobj(Fileobj=f, Bucket=bucket_name, Key=object_key)

    # list uploaded objects
    uploaded_objs = s3_client.list_objects(Bucket=bucket_name)
    print("Uploaded objects: ", uploaded_objs)

    # Retrieving object using presigned get

    get_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=3000,
        HttpMethod="GET",
    )
    print("Presigned Get Url: ", get_url)

    # Note: Bucket deletion using boto does not clean up bucket from the volume and may throw bucket exists error
    # if we're creating a bucket with the same name

    # Trying to uploading using PUT presigned Url
    # For reference: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    """
    object_key = "proflePut.html"
    response = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=3000,
        HttpMethod="PUT",
    )
    with open("profile2.html", "rb") as f:
        files = {"file": (object_key, f)}
        http_response = requests.put(response, files=files)
        print(http_response.status_code)  # Although this returns 200, but file is not uploaded correctly


    # Check uploaded objects
    uploaded_objs = s3_client.list_objects(Bucket=bucket_name)
    print("Uploaded objects: ", uploaded_objs)
    """

    """
    object_key = "profilePost.html"
    response = s3_client.generate_presigned_post(
        Bucket=bucket_name,
        Key=object_key,
        ExpiresIn=3600,
    )

    # Same issue here, sometime the status is 200 but the file is not reflected in the file system
    # or at least with the correct expected path
    with open(filename, "rb") as f:
        files = {"file": (object_key, f)}
        http_response = requests.post(response["url"], data=response["fields"], files=files)
        print(http_response.status_code)

    # Check uploaded objects
    uploaded_objs = s3_client.list_objects(Bucket=bucket_name)
    print("Uploaded objects: ", uploaded_objs)

    """


if __name__ == "__main__":
    # Create bucket
    create_bucket()

    # Upload file
    upload_file()

# stdlib
from datetime import datetime
import gc
from io import BytesIO
import sys
import time

# third party
import matplotlib.pyplot as plt
from minio import Minio
from minio.error import S3Error

"""
docker run -p 9000:9000 -p 9001:9001   quay.io/minio/minio server /data --console-address ":9001"
pip install minio
"""

files = [
    ("1GB", 1024 ** 3),
    ("5GB", (1024 ** 3) * 5),
    ("10GB", 1024 ** 3 * 10),
    ("15GB", 1024 ** 3 * 15),
]


def create_binary_data(length):
    header = bytes("Hello World!", "utf-8")
    return BytesIO(header + bytes(length - len(header)))


def send_data(data, file_name, length):
    before = datetime.now()
    obj = client.put_object("mystorage", file_name, data, length)
    after = datetime.now()
    diff = after - before
    return diff.total_seconds()


def get_data(file_name):
    before = datetime.now()
    obj = client.get_object("mystorage", file_name).read()
    print("Binary size: ", len(obj))
    after = datetime.now()
    diff = after - before
    return diff.total_seconds()


def delete_data(file_name):
    before = datetime.now()
    obj = client.remove_object("mystorage", file_name)
    after = datetime.now()
    diff = after - before
    return diff.total_seconds()


client = Minio(
    "10.0.2.15:9000", access_key="minioadmin", secret_key="minioadmin", secure=False
)


if not client.bucket_exists("mystorage"):
    print("Creating new bucket ...")
    client.make_bucket("mystorage")


def benchmark(operation_name):
    timestamp = {}
    operation = {
        "send": send_data,
        "get": get_data,
        "delete": delete_data,
    }
    print(" Operation: ", operation_name.upper())
    for file_name, length in files:
        print("Creating ", file_name, " ...")
        if operation_name == "send":
            data = create_binary_data(length)
            print(" Operation: ", operation_name.upper())
            timestamp[file_name] = operation[operation_name](data, file_name, length)
        else:
            timestamp[file_name] = operation[operation_name](file_name)
        gc.collect()

    plt.bar(list(timestamp.keys()), list(timestamp.values()))
    plt.title(operation_name)
    plt.xlabel("Data Size")
    plt.ylabel("Timestamp (s)")
    plt.savefig(operation_name + ".png")


if __name__ == "__main__":
    operation = sys.argv[1]
    benchmark(operation)

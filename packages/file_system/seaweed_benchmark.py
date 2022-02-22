# stdlib
from datetime import datetime
import gc
from io import BytesIO
import json

# third party
import matplotlib.pyplot as plt
import requests
from weed import operation
from weed.master import WeedMaster
from weed.util import put_file

"""
docker run -p 9333:9333 -p 19333:19333 --name master chrislusf/seaweedfs master
docker run -it -p 8080:8080 -p 18080:18080 -v `pwd`/swfs_data:/data --name volume --link master chrislusf/seaweedfs volume -max=10 -mserver="master:9333" -port=8080 -publicUrl="127.0.0.1:8080"
pip install python-weed
"""

# client = WeedMaster(url_base="http://localhost:9333")
wo = operation.WeedOperation(master_url_base="http://localhost:9333")

files = [
    ("1GB", 1024 ** 3),
    ("5GB", 1024 ** 3 * 5),
    ("10GB", 1024 ** 3 * 10),
    ("15GB", 1024 ** 3 * 15),
]

chunk_size = 256 * 1024 ** 2


def create_binary_data(length):
    chunks = []
    header = bytes("Hello World!", "utf-8")
    n_chunks = int(length / chunk_size)
    print("Number of chunks: ", n_chunks)
    for i in range(n_chunks):
        chunks.append(BytesIO(header + bytes(chunk_size - len(header))))
    return chunks


def combine_chunks(fids, file_name, length):
    manifest = {
        "name": f"{file_name}-sample.txt",
        "mime": "text/html",
        "size": length,
        "chunks": fids,
    }

    new_fid = wo.acquire_new_fids()
    fid_url = wo.get_fid_full_url(new_fid[0], True)
    params = (
        ("cm", "true"),
        ("pretty", "yes"),
    )

    files = {
        "file": ("manifest.json", json.dumps(manifest)),
    }
    response = requests.post(fid_url, params=params, files=files)
    print(f"Combine status: {response.status_code}")
    return new_fid


def send_data(filename, length):
    chunks = create_binary_data(length)
    gc.collect()
    before = datetime.now()
    fids = []
    offset = 0
    # we pregenerate the fids because we need to use get_fid_full_url(public_url=True)
    new_fids = wo.acquire_new_fids(len(chunks))
    for i, chunk in enumerate(chunks):
        fid = new_fids[i]
        fid_full_url = wo.get_fid_full_url(
            fid, True
        )  # TODO: figure out publicUrl vs url issues
        wor = put_file(chunk, fid_full_url, "")
        fids.append({"fid": fid, "offset": offset, "size": chunk_size})
        offset += chunk_size

    fids = combine_chunks(fids, filename, length)
    after = datetime.now()
    diff = after - before
    del chunks
    gc.collect()
    return diff.total_seconds(), fids


def get_data(fids):
    before = datetime.now()
    obj = b""
    for fid in fids:
        fid_full_url = wo.get_fid_full_url(
            fid, True
        )  # TODO: figure out publicUrl vs url issues
        # data = wo.get(fid=fid)
        data = requests.get(fid_full_url).content
    after = datetime.now()
    diff = after - before
    del data
    gc.collect()
    return diff.total_seconds()


def delete_data(fids):
    before = datetime.now()
    for fid in fids:
        # obj = wo.delete(fid=fid)
        fid_full_url = wo.get_fid_full_url(
            fid, True
        )  # TODO: figure out publicUrl vs url issues
        r = requests.delete(fid_full_url)
        print(r.status_code)
    after = datetime.now()
    diff = after - before
    return diff.total_seconds()


def plot_graph(operation_name, timestamp):
    plt.bar(list(timestamp.keys()), list(timestamp.values()))
    plt.title(operation_name)
    plt.xlabel("Data Size")
    plt.ylabel("Timestamp (s)")
    plt.savefig(operation_name + ".png")
    plt.clf()


send_timestamps = {}
get_timestamps = {}
delete_timestamps = {}

for file_size in files:
    print("Testing : ", file_size[0])
    print("Sending ... ")
    send_timestamp, fids = send_data(file_size[0], file_size[1])
    gc.collect()
    print("Getting ...")
    get_timestamp = get_data(fids)
    gc.collect()
    print("Deleting ...")
    delete_timestamp = delete_data(fids)
    send_timestamps[file_size[0]] = send_timestamp
    get_timestamps[file_size[0]] = get_timestamp
    delete_timestamps[file_size[0]] = delete_timestamp
    gc.collect()

plot_graph("SEND", send_timestamps)
plot_graph("GET", get_timestamps)
plot_graph("DELETE", delete_timestamps)

from weed.master import WeedMaster
from weed import operation
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import gc
import sys

client  = WeedMaster()
wo = operation.WeedOperation()

files = [
        ("1GB", 1024 ** 3),
        ("5GB", 1024 ** 3 * 5),
        ("10GB", 1024 ** 3 * 10),
        ("15GB", 1024 ** 3 * 15)
]

chunk_size = 256 * 1024** 2
def create_binary_data(length):
    chunks = []
    header = bytes("Hello World!", "utf-8")
    n_chunks = int(length / chunk_size)
    print("Number of chunks: ", n_chunks)
    for i in range(n_chunks):
        chunks.append(BytesIO(header + bytes(chunk_size - len(header))))
    return chunks



def send_data(length):
    chunks = create_binary_data(length)
    gc.collect()
    before = datetime.now()
    fids = []
    for chunk in chunks:
        fids.append( wo.put(chunk).fid )
    after = datetime.now()
    diff = after - before
    return diff.total_seconds(), fids

def get_data(fids):
    before = datetime.now()
    obj = b''
    for fid in fids:
        wo.get_content(fid=fid)
    after = datetime.now()
    diff = after - before
    return diff.total_seconds()


def delete_data(fids):
    before = datetime.now()
    for fid in fids:
        obj = wo.delete(fid=fid)
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
    send_timestamp, fids = send_data(file_size[1])
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

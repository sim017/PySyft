# stdlib
import time
from typing import Any

# third party
import numpy as np
from pympler.asizeof import asizeof
import pytest

# syft absolute
import syft as sy
from syft.logger import debug

DOMAIN1_PORT = 9082


def size(obj: Any) -> int:
    return asizeof(obj) / (1024 * 1024)  # MBs


def highest() -> int:
    ii32 = np.iinfo(np.int32)
    # 2147483647
    return ii32.max


# This fails on Windows CI even though the same code works in a Jupyter Notebook
# on the same Windows CI machine.
# @pytest.mark.xfail
@pytest.mark.network
def test_large_message_size() -> None:
    domain_client = sy.login(
        email="info@openmined.org", password="changethis", port=DOMAIN1_PORT
    )

    ndim = 11300  # 510.76 MB

    # rabbitmq recommends max is 512 MB
    # rabbitmq.conf has max_message_size = 536870912

    x = np.zeros((ndim, ndim), dtype=np.int32)
    x_bytes = sy.serialize(x)
    mb_size = size(x_bytes)
    mb = f"{mb_size} MB"

    try:
        start_time = time.time()
        print(f"Sending {mb} sized message")
        x_ptr = x.send(domain_client, tags=[f"{x.shape}", mb])
        x_ptr.block_with_timeout(180)
        total_time = time.time() - start_time
        print(f"Took {total_time}")
        data_rate = mb_size / total_time
        print(f"Send transfer rate: {data_rate}")
    except Exception as e:
        total_time = time.time() - start_time
        print(f"Failed to send {x.shape} in {total_time}. {e}")
        raise e

    try:
        start_time = time.time()
        back = x_ptr.get()
        assert (back == x).all()
        total_time = time.time() - start_time
        data_rate = mb_size / total_time
        print(f"Return transfer rate: {data_rate}")
    except Exception as e:
        print(f"Failed to get data back. {e}")
        raise e

    assert False


def get_now():
    # stdlib
    from datetime import datetime

    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")


@pytest.mark.network
def test_large_dataset_size() -> None:
    print(f"test starting")
    domain_client = sy.login(
        email="info@openmined.org", password="changethis", port=DOMAIN1_PORT
    )

    ndim = 20_000

    x = np.zeros((ndim, ndim), dtype=np.int32)

    x_bytes = sy.serialize(x, to_bytes=True)
    mb_size = size(x_bytes)
    mb = f"{mb_size} MB"

    # print(x_bytes)
    print(mb_size)
    print(mb)

    try:
        start_time = time.time()
        print(get_now(), f"Sending {mb} sized message")
        print(get_now(), f"Calling domain_client.load_dataset with {mb_size}")
        domain_client.load_dataset(
            assets={"dataset_size_test": x},
            name="dataset size test",
            description=("test"),
            skip_checks=True,
        )
        print(get_now(), f"FINISHED load_dataset")
        # x_ptr.block_with_timeout(300)
        total_time = time.time() - start_time
        print(f"Took {total_time}")
        data_rate = mb_size / total_time
        print(f"Send transfer rate: {data_rate}")
    except Exception as e:
        total_time = time.time() - start_time
        print(f"Failed to send {x.shape} in {total_time}. {e}")
        raise e

    # try:
    #     start_time = time.time()
    #     back = x_ptr.get()
    #     assert (back == x).all()
    #     total_time = time.time() - start_time
    #     data_rate = mb_size / total_time
    #     print(f"Return transfer rate: {data_rate}")
    # except Exception as e:
    #     print(f"Failed to get data back. {e}")
    #     raise e

    assert False

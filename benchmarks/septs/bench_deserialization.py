import syft as sy
from .util import make_sept, generate_data
import pyperf
import functools

def create_bench_sept_deserialize(runner: pyperf.Runner, rows: int, columns: int, lower_bound, upper_bound):
    data = generate_data(rows, columns, lower_bound, upper_bound)
    serialized_sept = sy.serialize(make_sept(data, lower_bound, upper_bound), to_bytes=True)
    sy.deserialize(serialized_sept, from_bytes=True)
    runner.bench_func(f"deserialize_sept_rows_{rows}_columns_{columns}", sy.deserialize, serialized_sept, from_bytes=True)
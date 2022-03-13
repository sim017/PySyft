# future
from __future__ import annotations

# stdlib
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union
from typing import Tuple
from typing import Set
from typing import Dict
from typing import List
from typing import Deque
from collections import deque
from dis import dis

# third party
import flax
import jax
from jax import numpy as jnp
from numpy.random import randint
from scipy.optimize import shgo
from functools import partial


def create_lookup_tables(dictionary: dict) -> Tuple[List[str], dict, List[dict]]:
    index2key = [str(x) for x in dictionary.keys()]
    key2index = {key:i for i, key in enumerate(index2key)}
    # Note this maps to GammaTensor, not to GammaTensor.value as name may imply
    index2values = [dictionary[i] for i in index2key]

    return index2key, key2index, index2values


def create_new_lookup_tables(dictionary: dict) -> Tuple[Deque[str], dict, Deque[dict], Deque[Tuple[int, ...]]]:
    index2key = deque()
    key2index = {}
    index2values = deque()  # Note this maps to GammaTensor, not to GammaTensor.value as name may imply
    index2size = deque()
    for index, key in enumerate(dictionary.keys()):
        key = str(key)
        index2key.append(key)
        key2index[key] = index
        index2values.append(dictionary[key])
        index2size.append(len(dictionary[key]))

    return index2key, key2index, index2values, index2size


def no_op(x: Dict[str, GammaTensor]) -> Dict[str, GammaTensor]:
    """A Private input will be initialized with this function.
    Whenever you manipulate a private input (i.e. add it to another private tensor), the result will have a different
    function. Thus we can check to seee if the f
    """
    return x


@flax.struct.dataclass
class GammaTensor:
    value: jnp.array
    min_val: float = flax.struct.field(pytree_node=False)
    max_val: float = flax.struct.field(pytree_node=False)
    func: Callable = flax.struct.field(pytree_node=False, default_factory=lambda: no_op)
    id: str = flax.struct.field(
        pytree_node=False, default_factory=lambda: str(randint(0, 2**32 - 1))
    )
    state: dict = flax.struct.field(pytree_node=False, default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.state) == 0:
            self.state[self.id] = self

    def run(self, state: dict) -> Union[Callable]:
        # we hit a private input
        if self.func is no_op:
            return self.func(state[self.id].value)
        return self.func(state)

    def __add__(self, other: Any) -> GammaTensor:
        state = dict()
        state.update(self.state)

        if isinstance(other, GammaTensor):
            adder = lambda state: jnp.add(self.run(state), other.run(state))
            state.update(other.state)
            value = self.value + other.value
            min_val = self.min_val + other.min_val
            max_val = self.max_val + other.max_val
        else:
            adder = lambda state: jnp.add(self.run(state), other)
            value = self.value + other
            min_val = self.min_val + other
            max_val = self.max_val + other

        return GammaTensor(value=value, min_val=min_val, max_val=max_val,
                           func=adder, state=state)

    def sum(self) -> GammaTensor:
        sum = lambda state: jnp.sum(self.run(state))
        state = dict()
        state.update(self.state)

        value = jnp.sum(self.value)
        min_val = jnp.sum(self.min_val)
        max_val = jnp.sum(self.max_val)

        return GammaTensor(
            value=value, min_val=min_val, max_val=max_val, func=sum, state=state
        )

    def expand_dims(self, axis: int) -> GammaTensor:
        expand_dims = lambda state: jnp.expand_dims(self.run(state), axis)

        state = dict()
        state.update(self.state)

        return GammaTensor(
            value=jnp.expand_dims(self.value, axis),
            min_val=self.min_val,
            max_val=self.max_val,
            func=expand_dims,
            state=state,
        )

    def squeeze(self, axis: Optional[int] = None) -> GammaTensor:
        squeeze = lambda state: jnp.squeeze(self.run(state), axis)
        state = dict()
        state.update(self.state)
        return GammaTensor(
            value=jnp.squeeze(self.value, axis),
            min_val=self.min_val,
            max_val=self.max_val,
            func=squeeze,
            state=state,
        )

    def __len__(self) -> int:
        return len(self.value)

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.value.shape

    @property
    def lipschitz_bound(self) -> float:
        # TODO: Check if there are any functions for which lipschitz bounds shouldn't be computed
        # if dis(self.func) == dis(no_op):
        #     raise Exception

        print("Starting JAX JIT")
        fn = jax.jit(self.func)
        print("Traced self.func with jax's jit, now calculating gradient")
        grad_fn = jax.grad(fn)
        print("Obtained gradient, creating lookup tables")
        i2k, k2i, i2v, i2s = create_new_lookup_tables(self.state)

        print("created lookup tables, now getting bounds")
        i2minval = jnp.concatenate([x.min_val for x in i2v]).reshape(-1, 1)
        i2maxval = jnp.concatenate([x.max_val for x in i2v]).reshape(-1, 1)
        bounds = jnp.concatenate([i2minval, i2maxval], axis=1)
        print("Obtained bounds")
        sample_input = i2minval.reshape(-1)
        print("Obtained all inputs")

        def max_grad_fn(input_values):
            vectors = {}
            n = 0
            for i, size_param in enumerate(i2s):
                vectors[i2k[i]] = input_values[n:n + size_param]
                n += size_param

            grad_pred = grad_fn(vectors)

            m = 0
            for value in grad_pred.values():
                m = max(m, jnp.max(value))

            # return negative because we want to maximize instead of minimize
            return -m

        print("starting SHGO")
        res = shgo(max_grad_fn, bounds, iters=1, constraints=tuple())
        print("Ran SHGO")
        # return negative because we flipped earlier
        return -float(res.fun)
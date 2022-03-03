import numpy as np
from numpy.typing import ArrayLike
from dataclasses import dataclass
from .row_entity_phi import RowEntityPhiTensor as REPT
from .lazy_array import LazyArray as Lazy
from typing import Union


@dataclass
class RowTensor:
    child: ArrayLike
    min_vals: ArrayLike
    max_vals: ArrayLike
    subjects: ArrayLike
    row_type: str


def convert_rept(tensor: Union[REPT, RowTensor]) -> Union[RowTensor, REPT]:
    """ This method converts a REPT to RowTensor, or vice versa """

    if isinstance(tensor, RowTensor):
        # We will make use of the fact that the last value in RowTensor.shape is the number of rows, and the
        return REPT(
            rows=[tensor.child[..., row_index] for row_index in range(tensor.child.shape[-1])]
        )

    elif isinstance(tensor, REPT):
        # Need to double check if shape is correct
        return RowTensor(
            child=np.stack(tensor.child, axis=-1),
            min_vals=Lazy(tensor.min_vals, tensor.shape),
            max_vals=Lazy(tensor.max_vals, tensor.shape),
            subjects=tensor.entities,
            row_type="ndarray"
        )


    else:
        raise Exception(
            "This method wasn't built to support that conversion. Sorry!"
        )
import numpy as np
from numpy.typing import ArrayLike
from dataclasses import dataclass
from typing import Tuple
from typing import List


@dataclass()
class LazyArray:
    data: ArrayLike
    shape: Tuple[int, ...]
    
    def simple_assets_for_serde(self) -> List:
        return [self.data, self.shape]
    
    @staticmethod
    def deserialize_from_simple_assets(assets: List) -> LazyArray:
        return LazyArray(data=assets[0], shape=assets[1])
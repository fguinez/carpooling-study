from typing import Tuple, FrozenSet
from pydantic import BaseModel


class CarpoolingOut(BaseModel):
    """
    Schema for trips input
    """
    groups: Tuple[FrozenSet[int]]

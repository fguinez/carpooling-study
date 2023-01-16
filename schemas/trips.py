from typing import List, Optional, Tuple, Union
from pydantic import BaseModel


class Trip(BaseModel):
    """
    Schema for trip
    """
    id: Optional[int]
    region: str
    origin_x: float
    origin_y: float
    destination_x: float
    destination_y: float
    datetime: str
    datasource: str


class TripsIn(BaseModel):
    """
    Schema for trips input
    """
    trips: List[Trip]

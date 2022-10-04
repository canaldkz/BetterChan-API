from pydantic import BaseModel
from typing import Union, List


class Filter(BaseModel):
    tags: List[str]
    series: str
    author: str
    
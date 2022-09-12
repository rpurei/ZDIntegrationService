from pydantic import BaseModel
from typing import Union


class ConturAPIGet(BaseModel):
    type: str
    key: str
    inn: Union[str, None] = None
    ogrn: Union[str, None] = None
    xml: bool = False

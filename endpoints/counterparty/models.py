from pydantic import BaseModel, validator
from typing import Union


class ConturAPIGet(BaseModel):
    api_key: str
    inn: Union[str, None] = None
    ogrn: Union[str, None] = None
    xml: bool = False


from pydantic import BaseModel, validator
from typing import Union


class ConturAPIGet(BaseModel):
    api_key: str
    inn: Union[str, None] = None
    ogrn: Union[str, None] = None
    xml: bool = False

    @validator('ogrn')
    def check_a_or_b(cls, v, values):
        if 'inn' not in values and not values['ogrn']:
            raise ValueError('either a or b is required')
        return values['ogrn']

from app_logger import logger
from .models import ConturAPIGet
from config import CONTUR_FOCUS_API_URL, CONTUR_FOCUS_API_VER, CONTUR_FOCUS_API_KEY, API_KEY
from fastapi import APIRouter, status, HTTPException
import requests
import traceback


router = APIRouter(
    prefix='/counterpartycheck',
    tags=['CounterpartyCheck'],
    responses={404: {'detail': 'Not found'}},
)


@router.get('/')
async def counterparty_check(input_data: ConturAPIGet):
    apikey_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='API key not valid'
    )
    badparams_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Request parameters not valid'
    )
    if input_data.api_key != API_KEY:
        logger.error(f'Error accessing API with: {str(input_data)}')
        raise apikey_exception
    try:
        pass
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{traceback.format_exc()} : {str(err)}')


if __name__ == '__main__':
    API_FUNCTION = '/req'
    final_url = CONTUR_FOCUS_API_URL + CONTUR_FOCUS_API_VER + API_FUNCTION
    params = {
                'key': CONTUR_FOCUS_API_KEY,
                'inn': '3123169789'
             }
    response_contur_api = requests.get(final_url, params=params)
    if response_contur_api.status_code == 200:
        print(response_contur_api.json())
    else:
        logger.error(f'Error getting ConturAPI request: {response_contur_api.status_code} - {response_contur_api.headers}')

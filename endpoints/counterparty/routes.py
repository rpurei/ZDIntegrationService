from app_logger import logger
from typing import Union
from config import CONTUR_FOCUS_API_URL, CONTUR_FOCUS_API_VER, CONTUR_FOCUS_API_KEY, API_KEY
from fastapi import APIRouter, status, HTTPException
import requests
import traceback
import json
import base64
from datetime import datetime
from pathlib import Path


router = APIRouter(
    prefix='/counterpartycheck',
    tags=['CounterpartyCheck'],
    responses={404: {'detail': 'Not found'}},
)


@router.get('/')
async def counterparty_check(api_key: str,
                             inn: Union[str, None] = None,
                             ogrn: Union[str, None] = None,
                             xml: bool = False):
    apikey_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='API key not valid'
    )
    badparams_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Request parameters not valid'
    )
    if api_key != API_KEY:
        logger.error(f'Error accessing API with: {api_key}')
        raise apikey_exception
    if not inn and not ogrn:
        logger.error(f'Both INN and OGRN empty')
        raise badparams_exception
    try:
        params = {
            'key': CONTUR_FOCUS_API_KEY
        }
        if inn:
            params['inn'] = inn
        if ogrn:
            params['ogrn'] = ogrn
        api_function_list = ['/req',
                             '/contacts',
                             '/sites',
                             '/egrDetails',
                             '/analytics',
                             '/briefReport',
                             '/finan',
                             '/beneficialOwners',
                             '/excerpt']
        result_report = {
            'BasicReport': {'Info': '',
                            'Phones': '',
                            'Sites': ''},
            'ExtendedReport_1': '',
            'ExtendedReport_2': '',
            'BasicPDFReport': '',
            'FinPDFReport': '',
            'BenefitiarsReport': {'Capital': '',
                                  'Benefitiars': '',
                                  'Benefitiars history': ''},
            'FNSPDFReport': ''
        }
        for api_index, api_function in enumerate(api_function_list):
            final_url = CONTUR_FOCUS_API_URL + CONTUR_FOCUS_API_VER + api_function
            if api_index == 5:
                params['pdf'] = ''
            if api_index == 6:
                del params['pdf']
            response_contur_api = requests.get(final_url, params=params)
            json_result = {}
            if response_contur_api.status_code == 200:
                try:
                    if api_index != 5 and api_index != 6 and response_contur_api.headers['content-type'].strip().startswith('application/json'):
                        json_result = response_contur_api.json()[0]
                    if api_index == 0:
                        result_report['BasicReport']['INN'] = json_result.get('inn')
                        result_report['BasicReport']['OGRN'] = json_result.get('ogrn')
                        result_report['BasicReport']['Info'] = json_result.get('UL')
                    if api_index == 1:
                        result_report['BasicReport']['Phones'] = json_result.get('contactPhones').get('phones')
                    if api_index == 2:
                        result_report['BasicReport']['Sites'] = json_result.get('sites')
                    if api_index == 3:
                        result_report['ExtendedReport_1'] = json_result
                    if api_index == 4:
                        result_report['ExtendedReport_2'] = json_result
                    if api_index == 5:
                        result_report['BasicPDFReport'] = base64.b64encode(response_contur_api.content)
                    if api_index == 6:
                        result_report['FinPDFReport'] = base64.b64encode(response_contur_api.content)
                    if api_index == 7:
                        result_report['BenefitiarsReport']['Capital'] = json_result.get('statedCapital')
                        result_report['BenefitiarsReport']['Benefitiars'] = json_result.get('beneficialOwners')
                        result_report['BenefitiarsReport']['Benefitiars history'] = json_result.get('historicalBeneficialOwners')
                    if api_index == 8:
                        result_report['FNSPDFReport'] = base64.b64encode(response_contur_api.content)
                except (ValueError, json.JSONDecodeError) as err:
                    logger.error(f'Error getting ConturAPI data: {json_result} status code: {response_contur_api.status_code} error: {str(err)} URL: {final_url} parameters: {params}')
            else:
                logger.error(f'Error getting ConturAPI request: {response_contur_api.status_code} - {response_contur_api.headers}')
        return result_report
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")} : {str(err)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{traceback.format_exc()} : {str(err)}')


if __name__ == '__main__':
    pass

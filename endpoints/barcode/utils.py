from app_logger import logger
from config import (DIRECTUM_API_USER, DIRECTUM_API_PASSWORD, DIRECTUM_PROTOCOL, DIRECTUM_URL, DIRECTUM_API_URL,
                    DIRECTUM_ATTACH_SET_URL)
import requests
import base64

headers = {'Username': DIRECTUM_API_USER,
           'Password': DIRECTUM_API_PASSWORD,
           'Content-Type': 'application/json',
           'Accept': 'application/json',
           'Return': 'representation',
           'Culture': 'ru-RU'}

set_attachment_version_uri = (DIRECTUM_PROTOCOL +
                              DIRECTUM_URL +
                              DIRECTUM_API_URL +
                              DIRECTUM_ATTACH_SET_URL
                              )


def doc_to_base64(file_name: str):
    encoded_string = ''
    try:
        with open(file_name, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
    except Exception as err:
        logger.error(f'For file:"{file_name}" error "{str(err)}" occured!!!')
    finally:
        return encoded_string


def doc_send_directum(doc_id: int, doc_string: str, doc_extension: str):
    response_directum_add_ver = ''
    payload_directum = {'docID': f'{doc_id}',
                        'docString': f'{doc_string}',
                        'docExtension': f'{doc_extension}'
                        }
    try:
        response_directum_add_ver = requests.post(set_attachment_version_uri,
                                                  data=payload_directum,
                                                  headers=headers)

    except Exception as err:
        logger.error(f'For document ID:"{doc_id}" error "{str(err)}" occured!!!')
    finally:
        logger.info(f'For document ID:"{doc_id}" created version response code "{response_directum_add_ver}"')
        return response_directum_add_ver.status_code

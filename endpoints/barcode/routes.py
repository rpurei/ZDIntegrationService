from app_logger import logger
from config import API_KEY, TEMP_NAME_LENGTH, TEMP_DIR
from .models import Document, DocumentResponse
from .barcode import make_qr
from .document import add_doc_header_picture, add_pdf_header_picture
from .utils import doc_to_base64, doc_send_directum
from fastapi import APIRouter, status, HTTPException
from pathlib import Path
import random
import string
import base64
import traceback

router = APIRouter(
    prefix='/barcode',
    tags=['Barcode'],
    responses={404: {'detail': 'Not found'}},
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=DocumentResponse)
async def add_category(input_document: Document):
    temp_qr_file = ''
    apikey_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='API key not valid'
    )
    if input_document.api_key != API_KEY:
        logger.error(f'Error accessing API with: {str(input_document)}')
        raise apikey_exception
    try:
        if input_document.doc_content == '' or input_document.doc_ext == '':
            raise ValueError
        temp_file_name = ''.join(random.choices(string.ascii_lowercase +
                                                string.digits,
                                                k=TEMP_NAME_LENGTH)) + f'.{input_document.doc_ext}'
        temp_dir = Path(TEMP_DIR)
        temp_full_name = temp_dir / temp_file_name
        with open(temp_full_name, 'wb+') as f:
            f.write(base64.b64decode(input_document.doc_content.encode('ascii')))
        temp_qr_file = make_qr(input_document.doc_qr_text)
        if temp_qr_file == '':
            raise ValueError()
        if input_document.doc_ext.startswith('doc') or input_document.doc_ext.startswith('pdf'):
            if add_doc_header_picture(str(temp_full_name), temp_qr_file) == -1:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f'Unsupported document type')
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unsupported document type')
        doc_base64 = doc_to_base64(str(temp_full_name))
        if len(doc_base64) > 0:
            doc_send_directum(input_document.doc_id, doc_base64, input_document.doc_ext)
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{traceback.format_exc()}')
    finally:
        Path(temp_qr_file).unlink()
        return {'detail': 'QR_INSERTED'}

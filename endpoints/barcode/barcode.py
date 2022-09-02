from app_logger import logger
from config import TEMP_DIR, TEMP_NAME_LENGTH
import qrcode
import random
import string
from pathlib import Path
import traceback


def make_qr(qr_text: str):
    qr_full_name = ''
    try:
        qr_file_name = ''.join(random.choices(string.ascii_lowercase +
                                              string.digits,
                                              k=TEMP_NAME_LENGTH)) + f'.png'
        qr_temp_dir = Path(TEMP_DIR)
        qr_full_name = qr_temp_dir / qr_file_name
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_H,
                           box_size=6,
                           border=2)
        qr.add_data(qr_text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color='black', back_color='white')
        qr_img.save(qr_full_name)
    except Exception as err:
        lf = '\n'
        logger.error(f'{traceback.format_exc().replace(lf, "")}')
    return qr_full_name


if __name__ == "__main__":
    make_qr('Purey Roman Pavlovich')

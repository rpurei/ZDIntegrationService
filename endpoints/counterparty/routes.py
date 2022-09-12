#from .models import ConturAPIGet
from config import CONTUR_FOCUS_API_URL, CONTUR_FOCUS_API_VER, CONTUR_FOCUS_API_KEY
import requests


if __name__ == '__main__':
    API_FUNCTION = '/stat'
    final_url = CONTUR_FOCUS_API_URL + CONTUR_FOCUS_API_VER + API_FUNCTION
    params = {
                'key': CONTUR_FOCUS_API_KEY
             }
    response_contur_api = requests.get(final_url, params=params)
    if response_contur_api.status_code == 200:
        print(response_contur_api.json())
import requests

from config import OPTIMIA_BI_MS_API_URL

base_url = OPTIMIA_BI_MS_API_URL

# Create User
def get_bi_info(cliente):

    url = base_url + '/stats'
    params = {
        "cliente": cliente
    }

    response = requests.get(url, params=params)

    return response
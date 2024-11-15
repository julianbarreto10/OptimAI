import requests

from config import OPTIMIA_DRIVERS_MS_API_URL

base_url = OPTIMIA_DRIVERS_MS_API_URL

# Create User
def create_driver(data):

    url = base_url + '/api/driver'

    response = requests.post(url, json=data)

    return response
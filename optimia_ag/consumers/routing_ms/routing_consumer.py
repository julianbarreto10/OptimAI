import requests

from config import OPTIMIA_ROUTING_MS_API_URL

base_url = OPTIMIA_ROUTING_MS_API_URL

# Create User
def create_routing(data):

    url = base_url + '/logysto_router'

    response = requests.post(url, json=data)

    return response
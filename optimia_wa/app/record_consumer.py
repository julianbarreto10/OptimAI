import requests

from app.config import ISBN_AG_API_URL

base_url = ISBN_AG_API_URL

# Create Record
def create_record(data):

    url = base_url + '/api/record'

    response = requests.post(url, json=data)

    return str(response.json())
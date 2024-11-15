import requests

def fetch_routing_data(cliente,url):
    # Llama a la API externa para obtener los datos de enrutamiento
    url += f"?cliente={cliente}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []
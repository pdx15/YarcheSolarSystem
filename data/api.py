import requests

BASE_URL = "https://api.le-systeme-solaire.net/rest/bodies/"

def get_body_info(name):
    try:
        r = requests.get(BASE_URL + name.lower())
        data = r.json()

        return f"{name}\nТип: {data.get('bodyType')}\nРадиус: {data.get('meanRadius')} km"
    except:
        return name
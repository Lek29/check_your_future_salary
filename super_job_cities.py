import requests
from pprint import pprint

SUPERJOB_CITIES_URL = 'https://api.superjob.ru/2.0/towns/'

response = requests.get(SUPERJOB_CITIES_URL)
response.raise_for_status

cities = response.json()
for city in cities['objects']:
    if city['title'] == 'Москва':
        print(f'Код Москвы:{city["id"]}')
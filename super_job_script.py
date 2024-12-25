from dotenv import load_dotenv
import os
import requests
from pprint import pprint

load_dotenv()

SUPER_JOB_KEY = os.getenv('SUPER_JOB_KEY')
SUPER_JOB_URL = 'https://api.superjob.ru/2.0/vacancies/'

headers = {
    'X-Api-App-Id': f'{SUPER_JOB_KEY}'
}

params = {
    'catalogues': 48,
    'town': 4,
    'count': 10,
}

response = requests.get(SUPER_JOB_URL, headers=headers, params=params)
response.raise_for_status()
vacancies = response.json()
if'objects' in vacancies:
    for vacancy in vacancies['objects']:
        pprint(f'{vacancy["profession"]}, {vacancy["town"]["title"]}')
else:
    print('Нет objects в vacancies')
    pprint(vacancies)
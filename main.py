import requests
from pprint import pprint


base_url = 'https://api.hh.ru/vacancies'

date_from = '2024-12-01'

vacancies_count = {}

params_all= {
    'text': f'программист Python',
    'area': 1,
    'per_page': 50,
    'page':0,
}
vacansies_all = requests.get(base_url, params=params_all)
vacansies_all.raise_for_status()
vacansies_all_json = vacansies_all.json()
for vacancy in vacansies_all_json['items']:
    salary = vacancy.get('salary', None)
    if salary:
        print({
            'from': salary.get('from', None),
            'to': salary.get('to', None),
            'currency': salary.get('currency', None),
            'gross': salary.get('gross', None)
        })




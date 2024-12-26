from dotenv import load_dotenv
import os
import requests
import math
from utils import predict_salary
from terminaltables import AsciiTable

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


def predict_rub_salary_for_superJob(vacancy):
    if vacancy['currency'] == 'rub':
        return predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
    return None
        

def get_all_vacancies_sj(language):
    all_salaries = []
    page = 0
    per_page = 100
    total_pages = 1

    while page < total_pages:
        params = {
            'keyword': f'Программист {language}',
            'catalogues': 48,  
            'town': 4,  
            'count': per_page,
            'page': page,
        }

        headers = {
                    'X-Api-App-Id': f'{SUPER_JOB_KEY}'
        }

        response = requests.get(SUPER_JOB_URL, headers=headers, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        total_pages = math.ceil(salaries_in_one_language['total'] / per_page)
        # print(f"Загружаем вакансии для {language}, страница {page + 1} из {total_pages}")

        for vacancy in salaries_in_one_language['objects']:
            salary_prediction = predict_rub_salary_for_superJob(vacancy)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
    return all_salaries, salaries_in_one_language['total']
    
def salary_in_languages_sj(languages):
    statistic = {}

    for language in languages:
        salaries, vacancies_found = get_all_vacancies_sj(language)
        filtred_salaries = [salary for salary in salaries if salary is not None]
        vacancies_processed = len(filtred_salaries)

        if vacancies_processed > 0:
            average_salary = int(sum(filtred_salaries) / vacancies_processed)
        else:
            average_salary = 0

        statistic[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }

    return statistic   

def print_statistics_table(statistics, title):
    
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]

    for language, stats in statistics.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ])

    
    table = AsciiTable(table_data)
    table.title = 'Вакансии SuperJob'

    print(table.table)

# languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']
# statistic_sj = salary_in_languages_sj(languages)
# print_statistics_table(statistic_sj, 'SuperJob Moscow')

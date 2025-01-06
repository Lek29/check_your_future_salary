from dotenv import load_dotenv
import os
import requests
import math
from utils import predict_salary
from utils import print_statistics_table
from terminaltables import AsciiTable
from pprint import pprint

load_dotenv()

SUPER_JOB_KEY = os.getenv('SUPER_JOB_KEY')
SUPER_JOB_URL = 'https://api.superjob.ru/2.0/vacancies/'
IT_CATALOGUE_ID = 48  
MOSCOW_TOWN_ID = 4
VACANCIES_PER_PAGE = 100

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
    """Вычисляет зарплату в рублях для вакансии с SuperJob.

    Args:
        vacancy (dict): Данные о вакансии из API SuperJob.

    Returns:
        float or None: Зарплата в рублях или None, если данные отсутствуют или валюта не rub.
    """
    if vacancy['currency'] == 'rub':
        return predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
    return None
        

def get_all_vacancies_sj(language):
    """Получает все вакансии для указанного языка программирования с SuperJob.

    Args:
        language (str): Язык программирования.

    Returns:
        tuple: (Список зарплат, общее количество найденных вакансий).
    """
    all_salaries = []
    page = 0
    
    while True:
        params = {
            'keyword': f'Программист {language}',
            'catalogues': IT_CATALOGUE_ID,  
            'town': MOSCOW_TOWN_ID,  
            'count': VACANCIES_PER_PAGE,
            'page': page,
        }

        headers = {
                    'X-Api-App-Id': f'{SUPER_JOB_KEY}'
        }

        response = requests.get(SUPER_JOB_URL, headers=headers, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        total_pages = math.ceil(salaries_in_one_language['total'] / VACANCIES_PER_PAGE)
        

        for vacancy in salaries_in_one_language['objects']:
            salary_prediction = predict_rub_salary_for_superJob(vacancy)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1

        if page >= total_pages:
            break

    return all_salaries, salaries_in_one_language['total']


def calculate_salary_in_languages_sj(languages):
    """Собирает статистику по зарплатам для языков программирования с SuperJob.

    Args:
        languages (list): Список языков программирования.

    Returns:
        dict: Статистика по каждому языку в формате:
            {
                'language': {
                    'vacancies_found': int,
                    'vacancies_processed': int,
                    'average_salary': int
                }
            }
    """
    statistic = {}

    for language in languages:
        salaries, vacancies_found = get_all_vacancies_sj(language)
        vacancies_processed = len(salaries)

        if vacancies_processed:
            average_salary = int(sum(salaries) / vacancies_processed)
        else:
            average_salary = 0

        statistic[language] = {
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary,
        }

    return statistic   


# def print_statistics_table(statistics):
#     """Выводит таблицу со статистикой по вакансиям с SuperJob.

#     Args:
#         statistics (dict): Статистика по вакансиям в формате:
#             {
#                 'language': {
#                     'vacancies_found': int,
#                     'vacancies_processed': int,
#                     'average_salary': int
#                 }
#             }
#     """
#     table_data = [
#         ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
#     ]

#     for language, stats in statistics.items():
#         table_data.append([
#             language,
#             stats['vacancies_found'],
#             stats['vacancies_processed'],
#             stats['average_salary']
#         ])

    
#     table = AsciiTable(table_data)
#     table.title = 'Вакансии SuperJob'

#     print(table.table)



import requests
from pprint import pprint
from utils import predict_salary
from utils import get_all_vacancies_hh


base_url_hh = 'https://api.hh.ru/vacancies'

def predict_rub_salary_hh(vacancy):
    if not vacancy:
        return None
    
    salary = vacancy.get('salary')
    if salary and salary.get('currency') == 'RUR':
        return predict_salary(salary.get('from'), salary.get('to'))
    

def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') == 'rub':
        return predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
    

def salary_in_languages(languages):
    statistic = {}

    for language in languages:
        salaries, vacancies_found = get_all_vacancies_hh(language)
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

def get_all_vacancies_hh(language):
    all_salaries = []
    page = 0
    per_page = 100
    total_pages = 1

    while page < total_pages:
        params = {
            'text': f'Программист {language}',
            'area': 1,
            'per_page': per_page,
            'page': page,
        }

        response = requests.get(base_url_hh, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        total_pages = salaries_in_one_language['pages']
        print(f"Загружаем вакансии для {language}, страница {page + 1} из {total_pages}")

        for vacancy in salaries_in_one_language['items']:
            salary = vacancy.get('salary')
            salary_prediction = predict_rub_salary_hh(salary)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
    return all_salaries, salaries_in_one_language['found']


languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']

pprint(salary_in_languages(languages))


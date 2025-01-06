import requests
from dotenv import load_dotenv
from pprint import pprint
from utils import print_statistics_table, predict_salary
from super_job_script import calculate_salary_in_languages_sj


BASE_URL_HH = 'https://api.hh.ru/vacancies'
MOSCOW_REGION_ID = 1
VACANCIES_PER_PAGE = 100 
    

def predict_rub_salary_hh(salary):
    """Вычисляет зарплату в рублях для вакансии с HeadHunter.

    Args:
        salary (dict or None): Данные о зарплате из API HeadHunter.

    Returns:
        float or None: Зарплата в рублях или None, если данные отсутствуют или валюта не RUR.
    """
    if not salary:
        return None
    
    if salary.get('currency') == 'RUR':
        predicted_salary = predict_salary(salary.get('from'), salary.get('to'))
        return predicted_salary
    
    return None


def predict_rub_salary_sj(vacancy):
    """Вычисляет зарплату в рублях для вакансии с SuperJob.

    Args:
        vacancy (dict): Данные о вакансии из API SuperJob.

    Returns:
        float or None: Зарплата в рублях или None, если данные отсутствуют или валюта не RUR.
    """
    if vacancy.get('currency') == 'RUR':
        return predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
    


def calculate_salary_in_languages_hh(languages):
    """Собирает статистику по зарплатам для языков программирования с HeadHunter.

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
        salaries, vacancies_found = get_all_vacancies_hh(language)
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

 
def get_all_vacancies_hh(language):
    """Получает все вакансии для указанного языка программирования с HeadHunter.

    Args:
        language (str): Язык программирования.

    Returns:
        tuple: (Список зарплат, общее количество найденных вакансий).
    """
    all_salaries = []
    page = 0
    per_page = VACANCIES_PER_PAGE
    

    while True:
        params = {
            'text': f'Программист {language}',
            'area': MOSCOW_REGION_ID,
            'per_page': per_page,
            'page': page,
        }

        response = requests.get(BASE_URL_HH, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        total_pages = salaries_in_one_language['pages']

        for vacancy in salaries_in_one_language['items']:
            salary = vacancy.get('salary')
            salary_prediction = predict_rub_salary_hh(salary)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
        if page >= total_pages:
            break

    return all_salaries, salaries_in_one_language['found']


def main():
    load_dotenv()
    
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']
    statistic_hh = calculate_salary_in_languages_hh(languages)
    print_statistics_table(statistic_hh, 'Вакансии HH')

    statistic_sj = calculate_salary_in_languages_sj(languages)
    print_statistics_table(statistic_sj, 'Вакансии SuperJob')


if __name__ == '__main__':
    main()
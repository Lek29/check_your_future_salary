import requests
from pprint import pprint
from terminaltables import AsciiTable
from super_job_script import calculate_salary_in_languages_sj, print_statistics_table 


BASE_URL_HH = 'https://api.hh.ru/vacancies'


def predict_salary(salary_from, salary_to):
    """Вычисляет среднюю зарплату на основе нижней и верхней границ.

    Args:
        salary_from (int or None): Нижняя граница зарплаты.
        salary_to (int or None): Верхняя граница зарплаты.

    Returns:
        float or None: Средняя зарплата или None, если данные отсутствуют.
    """
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None
    

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


def print_statistic_table_hh(statistic):
    """Выводит таблицу со статистикой по вакансиям с HeadHunter.

    Args:
        statistic (dict): Статистика по вакансиям в формате:
            {
                'language': {
                    'vacancies_found': int,
                    'vacancies_processed': int,
                    'average_salary': int
                }
            }
    """
    table_data = [
        ['Язык программирования', 
         'Вакансий найдено',
         'Вакансий обработано', 
         'Средняя зарплата'],
    ]
    for language, stats in statistic.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary'],
        ])
    
    table = AsciiTable(table_data)
    table.title = 'Вакансии HH'

    print(table.table)

 
def get_all_vacancies_hh(language):
    """Получает все вакансии для указанного языка программирования с HeadHunter.

    Args:
        language (str): Язык программирования.

    Returns:
        tuple: (Список зарплат, общее количество найденных вакансий).
    """
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

        response = requests.get(BASE_URL_HH, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        for vacancy in salaries_in_one_language['items']:
            salary = vacancy.get('salary')
            salary_prediction = predict_rub_salary_hh(salary)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
    return all_salaries, salaries_in_one_language['found']


def main():
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']
    statistic_hh = calculate_salary_in_languages_hh(languages)
    print_statistic_table_hh(statistic_hh)

    statistic_sj = calculate_salary_in_languages_sj(languages)
    print_statistics_table(statistic_sj)


if __name__ == '__main__':
    main()
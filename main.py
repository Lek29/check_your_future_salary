import requests
from pprint import pprint
from terminaltables import AsciiTable
from super_job_script import salary_in_languages_sj, print_statistics_table 


base_url_hh = 'https://api.hh.ru/vacancies'


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None
    

def predict_rub_salary_hh(salary):
    if not salary:
        return None
    
    if salary.get('currency') == 'RUR':
        predicted_salary = predict_salary(salary.get('from'), salary.get('to'))
        return predicted_salary
    
    return None


def predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') == 'RUR':
        return predict_salary(vacancy.get('payment_from'), vacancy.get('payment_to'))
    


def salary_in_languages_hh(languages):
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

        for vacancy in salaries_in_one_language['items']:
            salary = vacancy.get('salary')
            salary_prediction = predict_rub_salary_hh(salary)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
    return all_salaries, salaries_in_one_language['found']


def main():
    languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']
    statistic_hh = salary_in_languages_hh(languages)
    print_statistic_table_hh(statistic_hh)

    statistic_sj = salary_in_languages_sj(languages)
    print_statistics_table(statistic_sj)


if __name__ == '__main__':
    main()
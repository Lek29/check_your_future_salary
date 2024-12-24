import requests
from pprint import pprint


base_url = 'https://api.hh.ru/vacancies'

date_from = '2024-12-01'

# vacancies_count = {}

# params_all= {
#     'text': f'программист Python',
#     'area': 1,
#     'per_page': 50,
#     'page':0,
# }
# vacansies_all = requests.get(base_url, params=params_all)
# vacansies_all.raise_for_status()
# vacansies_all_json = vacansies_all.json()
# for vacancy in vacansies_all_json['items']:
#     salary = vacancy.get('salary', None)
#     if salary:
#         print({
#             'from': salary.get('from', None),
#             'to': salary.get('to', None),
#             'currency': salary.get('currency', None),
#             'gross': salary.get('gross', None)
#         })
def predict_rub_salary(vacancy):
    params_all= {
    'text': f'{vacancy}',
    'area': 1,
    'per_page': 20,
    'page':0,
}
    salary_print = []
    vacancy_all = requests.get(base_url, params=params_all)
    vacancy_all.raise_for_status()
    vacancy_json = vacancy_all.json()

    for vacancy in vacancy_json['items']:
        salary = vacancy.get('salary')
        if salary and salary.get('currency') == 'RUR':
            salary_from = salary.get('from')
            salary_to = salary.get('to')    
            if salary_from and salary_to:
                average_salary = (salary_from + salary_to ) / 2
                salary_print.append(average_salary)
            elif salary_from:
                salary = salary.get('from') * 1.2
                salary_print.append(salary)
            elif  salary_to:
                    salary = salary.get('to') * 0.8
                    salary_print.append(salary)
            else:
                 salary_print.append(None)
        else:
             salary_print.append(None)
    
    return salary_print, vacancy_json['found']

     

def salary_in_languages(languages):
    statistic = {}

    for language in languages:
        salaries, vacancies_found = predict_rub_salary(f'Программист {language}')
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


languages = ['Python', 'Java', 'JavaScript', 'Ruby', 'PHP', 'C++', 'C#', 'Go', 'Swift', 'TypeScript']

pprint(salary_in_languages(languages))


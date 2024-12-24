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
def predict_rub_salary(salary):
    if salary and salary.get('currency') == 'RUR':
       if salary and salary.get('currency') == 'RUR':
        salary_from = salary.get('from')
        salary_to = salary.get('to')

        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        elif salary_from:
            return salary_from * 1.2
        elif salary_to:
            return salary_to * 0.8
    return None

def get_all_vacancies(language):
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

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        salaries_in_one_language = response.json()

        total_pages = salaries_in_one_language['pages']
        print(f"Загружаем вакансии для {language}, страница {page + 1} из {total_pages}")

        for vacancy in salaries_in_one_language['items']:
            salary = vacancy.get('salary')
            salary_prediction = predict_rub_salary(salary)
            if salary_prediction:
                all_salaries.append(salary_prediction)

        page += 1
    return all_salaries, salaries_in_one_language['found']


def salary_in_languages(languages):
    statistic = {}

    for language in languages:
        salaries, vacancies_found = get_all_vacancies(language)
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


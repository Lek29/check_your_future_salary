from terminaltables import AsciiTable

def print_statistics_table(statistic, title):
    """Выводит таблицу со статистикой по вакансиям.

    Args:
        statistic (dict): Статистика по вакансиям в формате:
            {
                'language': {
                    'vacancies_found': int,
                    'vacancies_processed': int,
                    'average_salary': int
                }
            }
        title (str): Заголовок таблицы.
    """
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for language, stats in statistic.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary'],
        ])
    
    table = AsciiTable(table_data)
    table.title = title
    print(table.table)

    
def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    else:
        return None
    
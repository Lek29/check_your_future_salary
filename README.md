# Анализ вакансий с HeadHunter и SuperJob

Этот проект предназначен для анализа вакансий с платформ HeadHunter (HH) и SuperJob (SJ) по различным языкам программирования. Скрипты собирают данные о вакансиях, вычисляют среднюю зарплату и выводят результаты в виде таблиц.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-username/ваш-репозиторий.git
   cd ваш-репозиторий
   ```
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Создайте файл `.env` в корне проекта и добавьте туда ваш API-ключ для SuperJob:
   ```
   SUPER_JOB_KEY=ваш_api_ключ
   ```
## Использование

Запустите основной скрипт:
  ```bash
  python main.py
  ```
Что делает скрипт:
Собирает данные о вакансиях с HeadHunter и SuperJob для следующих языков программирования:

- Python

- Java

- JavaScript

- Ruby

- PHP

- C++

- C#

- Go

- Swift

- TypeScript

Вычисляет среднюю зарплату для каждого языка программирования.

Выводит результаты в виде таблиц:

- Таблица с вакансиями с HeadHunter:

| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
|-----------------------|------------------|----------------------|------------------|
| Python                | 1000             | 800                  | 120000           |
| Java                  | 900              | 700                  | 110000           |
| JavaScript            | 850              | 650                  | 105000           |

- Таблица с вакансиями с SuperJob:

| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
|:----------------------|-----------------:|:--------------------:|-----------------:|
| Python                | 500              | 400                  | 115000           |
| Java                  | 450              | 350                  | 105000           |
| JavaScript            | 400              | 300                  | 100000           |
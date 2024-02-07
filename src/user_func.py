import json
import os
from config import VACANCY_FILTER_JSON_PATH, VACANCY_ALL_JSON_PATH
from src.hh_work_platforms import HeadHunterAPI
from src.json_saver import JSONSaver
from src.sj_work_platform import SuperJobAPI
from src.operations_for_vacancies import OperationsVacancies
from src.vacancy import Vacancy


def search_vacancies_in_json():
    """
    Функция взаимодействия с пользователем,
    фильтрация json файла с вакансиями по выбранным параметрам
    """
    while True:
        filter_user = input("Какие по каким критериям вы хотите получить вакансии:\n"
                            "1 - по совпадению слова в названии вакансии\n"
                            "2 - по совпадению города\n"
                            "3 - по названию компании\n"
                            "4 - по зарплате\n").strip()

        if not (filter_user in ["1", "2", "3", "4"]):
            print("\nВы ввели неверное значение попробуйте снова\n")
            continue

        with open(VACANCY_ALL_JSON_PATH, encoding='utf-8') as file:
            json_data = json.load(file)

        list_vacancy = [Vacancy(**item) for item in json_data]

        operations = OperationsVacancies()
        sorted_vacancies = operations.sort_vacancies(list_vacancy)
        index = 0

        if filter_user == "1":
            user_answer = input("Введите ключевое слово для поиска в названии вакансии: ").strip().lower()
            for item in sorted_vacancies:
                if user_answer in item.name.lower():
                    index += 1
                    print(f"{index}: {item}")
            if index == 0:
                print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос\n")
            else:
                break

        elif filter_user == "2":
            user_answer = input("Введите название города: ").strip().lower()
            for item in sorted_vacancies:
                if user_answer in item.area.lower():
                    index += 1
                    print(f"{index}: {item}")
            if index == 0:
                print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос\n")
            else:
                break

        elif filter_user == "3":
            user_answer = input("Введите название компании: ").strip().lower()

            for item in sorted_vacancies:
                company = item.employer.get('name')
                if company:
                    if user_answer == company.lower():
                        index += 1
                        print(f"{index}: {item}")
            if index == 0:
                print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос\n")
            else:
                break

        elif filter_user == "4":
            user_from, user_to = list(map(int, input("Введите диапазон зарплаты(пример 100000-150000): ").strip().split('-')))
            for item in sorted_vacancies:
                if item.salary:
                    index += 1
                    if item.from_salary and item.to_salary:
                        if item.from_salary == user_from and item.to_salary == user_to:
                            print(f"{index}: {item}")
                    elif item.from_salary and not item.to_salary:
                        if item.from_salary in range(user_from, user_to+1):
                            print(f"{index}: {item}")
                    elif not item.from_salary and item.to_salary:
                        if item.to_salary in range(user_from, user_to+1):
                            print(f"{index}: {item}")
            if index == 0:
                print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос\n")
            else:
                break
        else:
            print("Несуществующий параметр запроса")


def get_vacancy_in_platform():
    """Функция взаимодействие с пользователем, обращение к API по заданным параметрам"""
    search_platform = input("Выберите платформу для поиска\n"
                            "1 - HeadHunter\n"
                            "2 - SuperJob\n"
                            "(Нажмите Enter если выбрать обе платформы): ").strip()

    search_query = input("\nВведите поисковый запрос: ").strip()

    with_experience = input('\nВведите опыт работы(число лет)\n'
                            '(Нажмите Enter если искать вакансии с любым опытом): ').strip()

    with_salary = input('\nИскать вакансии с зарплатой введите:\n'
                        '1 - только где указана зарплата\n'
                        '(Нажмите Enter если искать все): ').strip()

    user_query = {'search_query': search_query,
                  'experience': with_experience,
                  'salary': with_salary}

    if search_platform == "1":
        platforms = ["HeadHunter"]
    elif search_platform == "2":
        platforms = ["SuperJob"]
    else:
        platforms = ["HeadHunter", "SuperJob"]

    if len(platforms) == 2:
        hh = HeadHunterAPI()
        sj = SuperJobAPI()
        hh.get_vacancies(**user_query)
        sj.get_vacancies(**user_query)
        vacancies_all = hh.vacancies + sj.vacancies
    elif platforms[0] == "HeadHunter":
        hh = HeadHunterAPI()
        hh.get_vacancies(**user_query)
        vacancies_all = hh.vacancies
    else:
        sj = SuperJobAPI()
        sj.get_vacancies(**user_query)
        vacancies_all = sj.vacancies

    filter_words = input("\nВведите ключевые слова(через пробел) для фильтрации вакансий\n"
                         "(Нажмите Enter чтобы искать без фильтра): ").lower().split()

    operations = OperationsVacancies()

    filtered_vacancies = operations.filter_vacancies(vacancies_all, filter_words)

    if not filtered_vacancies:
        print("\nНет вакансий, соответствующих заданным критериям.")
        exit()

    top_n = input("\nВведите количество вакансий которое вы хотите получить\n"
                  "(Нажмите Enter чтобы получить все): ").strip()

    sorted_vacancies = operations.sort_vacancies(filtered_vacancies)
    top_vacancies = operations.get_top_vacancies(sorted_vacancies, top_n)
    operations.print_vacancies(top_vacancies)

    save_list_vacancy = input("\nХотите ли сохранить вакансии:\n"
                              "1 - да\n"
                              "2 - нет\n")

    if save_list_vacancy.isdigit():
        answer_num = int(save_list_vacancy)
        if answer_num == 1:

            save = JSONSaver()
            save.file_path = VACANCY_FILTER_JSON_PATH
            for item in top_vacancies:
                save.add_vacancy(item)
            print("Данные сохранены. Выход.")
        else:
            print("Выход")
            exit()
    else:
        print("Выход")
        exit()


def user_interaction():
    """Стартовый диалог"""
    while True:
        user_get = input("Здравствуйте! Введите число и нажмите Enter:\n"
                         "1 - для получения вакансий от API\n"
                         "2 - для работы с существующим json файлом вакансий\n").strip()
        if user_get in ["1", "2"]:
            break
    if user_get == "1":
        get_vacancy_in_platform()
    elif user_get == "2":
        if not os.path.exists(VACANCY_ALL_JSON_PATH):
            print("Файла json не существует сначала получите вакансии от API\n")
            user_interaction()
        else:
            search_vacancies_in_json()

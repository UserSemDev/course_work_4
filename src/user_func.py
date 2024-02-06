from config import VACANCY_FILTER_JSON_PATH
from src.hh_work_platforms import HeadHunterAPI
from src.json_saver import JSONSaver
from src.sj_work_platform import SuperJobAPI
from src.operations_for_vacancies import OperationsVacancies


def user_interaction():
    """Взаимодействие с пользователем"""
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

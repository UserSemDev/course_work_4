class OperationsVacancies:

    @staticmethod
    def filter_vacancies(list_vacancy: list, filters: list) -> list:
        """
        Метод для фильтрации списка по ключевым словам
        :param list_vacancy: список вакансий для фильтрации
        :param filters: список ключевых слов для фильтрации
        :return: возвращает отфильтрованный список вакансий
        """
        if not filters:
            return list_vacancy

        filtered_vacancies = []
        for item in list_vacancy:
            description = item.description.lower()
            if all(word in description for word in filters):
                filtered_vacancies.append(item)
        return filtered_vacancies

    @staticmethod
    def sort_vacancies(list_vacancy: list) -> list:
        """
        Метод сортировки вакансий по зарплате
        :param list_vacancy: Список вакансий для сортировки
        :return: возвращает отсортированный список
        """
        return sorted(list_vacancy, reverse=True)

    @staticmethod
    def get_top_vacancies(list_vacancy: list, num: str) -> list:
        """
        Метод получения топ вакансий
        :param list_vacancy: список вакансий
        :param num: количество вакансий которое необходимо вернуть
        :return: возвращает список топ вакансий
        """
        if num == "":
            num = len(list_vacancy)
        elif num.isdigit():
            num = int(num)
        if 0 < len(list_vacancy) <= num:
            return list_vacancy
        else:
            return list_vacancy[0:num]

    @staticmethod
    def print_vacancies(list_vacancy: list) -> None:
        """
        Метод вывода вакансий
        :param list_vacancy: список вакансий для вывода
        """
        index = 0
        for item in list_vacancy:
            index += 1
            print(f"{index}: {item}")

from abc import ABC, abstractmethod


class JobVacancyAPI(ABC):
    """Абстрактный класс пря поиска вакансий через API"""

    @abstractmethod
    def get_vacancies(self, **kwargs: dict) -> None:
        """
        Абстрактный метод получения вакансий
        :param kwargs: полученные от пользователя параметры в виде словаря для запроса
        :return: None
        """
        pass

    @staticmethod
    def correct_query(user_params: dict) -> dict:
        """
        Статический метод корректировки запроса пользователя
        :param user_params: словарь пользователя с параметрами запроса
        :return: корректный словарь для запроса к API
        """
        pass

    @staticmethod
    def get_params_vacancy(job_item: dict) -> dict:
        """
        Метод возвращающий словарь с параметрами вакансии
        :param job_item: словарь полученный от API с параметрами вакансии
        :return: возвращаем словарь с нужными нам параметрами
        """
        pass
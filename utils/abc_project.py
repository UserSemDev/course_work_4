from abc import ABC, abstractmethod


class JobVacancyAPI(ABC):
    """Абстрактный класс пря поиска вакансий через API"""

    @abstractmethod
    def get_vacancies(self, **kwargs):
        """Абстрактный метод получения вакансий"""
        pass

    @staticmethod
    def correct_query(user_params: dict) -> dict:
        pass

    @staticmethod
    def get_params_vacancy(job_item: dict) -> dict:
        pass
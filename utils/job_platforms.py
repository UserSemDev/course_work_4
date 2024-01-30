from abc import ABC, abstractmethod


class JobVacancyAPI(ABC):

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass


class HeadHunterAPI(JobVacancyAPI):
    def get_vacancies(self, **kwargs):
        pass


class SuperJobAPI(JobVacancyAPI):
    def get_vacancies(self, **kwargs):
        pass
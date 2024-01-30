import random
import time
from abc import ABC, abstractmethod
import requests
from utils.exceptions import ResponseError


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
    def get_params_vacancy(job_item: dict, index: int) -> dict:
        pass


class HeadHunterAPI(JobVacancyAPI):
    """Класс для рабы с API HeadHunter"""

    url = 'https://api.hh.ru/vacancies/'

    def __init__(self) -> None:
        """Инициализация параметров для запроса к API"""
        self.params = {
            'text': '',
            'only_with_salary': False,
            'per_page': 100,
            'page': 0,
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

    def get_vacancies(self, **kwargs: dict) -> None:
        """
        Метод для получения вакансий с API HeadHunter
        :param kwargs: словарь полученный от пользователя с параметрами для запроса
        :return: None
        """
        data = self.correct_query(kwargs)
        self.params['text'] = data['search_query']
        self.params['only_with_salary'] = data['salary']
        if data.get('experience'):
            self.params['experience'] = data['experience']
        index = 0
        while True:
            try:
                response = requests.get(self.url, params=self.params, headers=self.headers)
                if response.status_code == 200:
                    resp = response.json()
                    items = resp['items']
                    found = resp['found']
                    page = resp['page']
                    pages = resp['pages']
                    for item in items:
                        index += 1
                        job_vacancy = self.get_params_vacancy(item, index)
                        print(job_vacancy)
                    if page == pages - 1:
                        break
                    self.params['page'] = self.params.get('page') + 1
                    random_time = random.uniform(0.2, 0.4)
                    time.sleep(random_time)
                else:
                    raise ResponseError(f'Ошибка запроса, статус код: [{response.status_code}]')
            except ResponseError as ex:
                print(ex)
                exit()

        print(f'Всего вакансий: {found}')

    @staticmethod
    def correct_query(user_params: dict) -> dict:
        """
        Метод обработки полученных от пользователя данных для обращения к API
        :param user_params: словарь с параметрами полученный от пользователя
        :return: откорректированный словарь параметров для запроса к API
        """
        dict_experience = {
            range(0, 1): 'noExperience',
            range(1, 3): 'between1And3',
            range(3, 6): 'between3And6',
            range(6, 100): 'moreThan6'
        }

        experience = user_params['experience']
        if experience.strip().isdigit():
            for key in dict_experience.keys():
                if int(experience) in key:
                    user_params['experience'] = dict_experience[key]
        else:
            del user_params['experience']

        salary = user_params['salary']
        if salary.isdigit():
            salary = int(salary)
            data = True if salary == 1 else False
        else:
            data = False
        user_params['salary'] = data

        return user_params

    @staticmethod
    def get_params_vacancy(job_item: dict, index: int) -> dict:
        """
        Метод получающий параметры вакансии и возвращающий словарь
        :param job_item: json словарь полученный от API с вакансией
        :param index: счетчик вакансий
        :return: возвращает словарь с вакансией
        """
        name = job_item['name']
        if job_item['salary']:
            salary = {'from': job_item['salary']['from'],
                      'to': job_item['salary']['to'],
                      'currency': job_item['salary']['currency']}
        else:
            salary = None
        experience = job_item.get('experience').get('name')
        employer = {
            'name': job_item.get('employer').get('name'),
            'alternate_url': job_item.get('employer').get('alternate_url')
        }
        alternate_url = job_item.get('alternate_url')
        data = {'id': index,
                'name': name,
                'salary': salary,
                'experience': experience,
                'employer': employer,
                'url_vacancy': alternate_url}
        return data


class SuperJobAPI(JobVacancyAPI):
    def get_vacancies(self, **kwargs):
        """Метод для получения вакансий с API SuperJob"""
        pass
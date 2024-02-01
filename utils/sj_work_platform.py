import os
import random
import time
import requests
from utils.abc_project import JobVacancyAPI
from utils.exceptions import ResponseError
from utils.vacancy import Vacancy


class SuperJobAPI(JobVacancyAPI):

    url = 'https://api.superjob.ru/2.0/vacancies/'
    SJ_API_KEY = os.getenv('SUPER_JOB_API_KEY')

    def __init__(self) -> None:
        """Инициализация параметров для запроса к API"""
        self.vacancies = []
        self.params = {
            'keyword': None,
            'count': 100,
            'page': 0,
        }

        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": self.SJ_API_KEY,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }

    def get_vacancies(self, **kwargs):
        """Метод для получения вакансий с API SuperJob"""
        data = self.correct_query(kwargs)
        self.params['keyword'] = data['search_query']
        if data.get('salary'):
            self.params['payment_defined'] = data['salary']
        if data.get('experience'):
            self.params['experience'] = data['experience']
        index = 0
        while True:
            try:
                response = requests.get(self.url, params=self.params, headers=self.headers)
                if response.status_code == 200:
                    resp = response.json()
                    items = resp['objects']
                    page = resp['more']
                    for item in items:
                        job_vacancy = self.get_params_vacancy(item)
                        self.vacancies.append(Vacancy(**job_vacancy))
                    print(f'Загружены вакансии. Страница {index + 1}')
                    if page is False:
                        break
                    self.params['page'] = self.params.get('page') + 1
                    random_time = random.uniform(0.2, 0.4)
                    time.sleep(random_time)
                else:
                    raise ResponseError(f'Ошибка запроса, статус код: [{response.status_code}]')
            except ResponseError as ex:
                print(ex)
                continue
        print(f'Всего вакансий получено с sj: {len(self.vacancies)}')

    @staticmethod
    def correct_query(user_params: dict) -> dict:
        """
        Метод обработки полученных от пользователя данных для обращения к API
        :param user_params: словарь с параметрами полученный от пользователя
        :return: откорректированный словарь параметров для запроса к API
        """
        dict_experience = {
                range(0, 1): "1",  # "без опыта"
                range(1, 3): "2",  # "от 1 года"
                range(3, 6): "3",  # "от 3 лет"
                range(6, 100): "4"  # "от 6 лет"
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
            if salary == 1:
                user_params['salary'] = 1
            else:
                del user_params['salary']
        else:
            del user_params['salary']

        return user_params

    @staticmethod
    def get_params_vacancy(job_item):
        """
        Метод получающий параметры вакансии и возвращающий словарь
        :param job_item: json словарь полученный от API с вакансией
        :return: возвращает словарь с вакансией
        """
        id_vacancy = job_item['id']
        name = job_item['profession']
        if job_item['payment_from'] != 0 or job_item['payment_to'] != 0:
            currency = 'RUR' if job_item['currency'].upper() == 'RUB' else job_item['currency'].upper()
            salary = {'from': job_item['payment_from'],
                      'to': job_item['payment_to'],
                      'currency': currency}
        else:
            salary = None
        experience = job_item.get('experience').get('title')
        employer = {
            'name': job_item.get('client').get('title'),
            'alternate_url': job_item.get('client').get('url')
        }
        alternate_url = job_item.get('link')
        data = {'id': id_vacancy,
                'name': name,
                'salary': salary,
                'experience': experience,
                'employer': employer,
                'url_vacancy': alternate_url,
                'platform': 'SuperJob'}
        return data
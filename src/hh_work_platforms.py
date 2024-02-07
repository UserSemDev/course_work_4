import random
import time
import requests
from src.abc_project import JobVacancyAPI
from src.exceptions import ResponseError
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


class HeadHunterAPI(JobVacancyAPI):
    """Класс для рабы с API HeadHunter"""

    url = 'https://api.hh.ru/vacancies/'

    def __init__(self) -> None:
        """Инициализация параметров для запроса к API"""
        self.vacancies = []
        self.params = {
            'text': None,
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
        while True:
            try:
                response = requests.get(self.url, params=self.params, headers=self.headers)
                if response.status_code == 200:
                    resp = response.json()
                    items = resp['items']
                    page = resp['page']
                    pages = resp['pages']
                    for item in items:
                        job_vacancy = self.get_params_vacancy(item)
                        vacancy = Vacancy(**job_vacancy)
                        self.vacancies.append(vacancy)
                        json_saver = JSONSaver()
                        json_saver.add_vacancy(vacancy)
                    print(f'Загружены вакансии. Страница {page + 1} из {pages}')
                    if page == pages - 1:
                        break
                    self.params['page'] = self.params.get('page') + 1
                    random_time = random.uniform(0.2, 0.4)
                    time.sleep(random_time)
                else:
                    raise ResponseError(f'Ошибка запроса, статус код: [{response.status_code}]')
            except ResponseError as ex:
                print(ex)
                continue
        print(f'Всего вакансий получено c hh: {len(self.vacancies)}')

    @staticmethod
    def correct_query(user_params: dict) -> dict:
        """
        Метод обработки полученных от пользователя данных для обращения к API
        :param user_params: словарь с параметрами полученный от пользователя
        :return: откорректированный словарь параметров для запроса к API
        """
        dict_experience = {
            range(0, 1): {'id': 'noExperience', 'name': "без опыта"},
            range(1, 3): {'id': 'between1And3', 'name': "от 1 до 3 лет"},
            range(3, 6): {'id': 'between3And6', 'name': "от 3 до 6 лет"},
            range(6, 100): {'id': 'moreThan6', 'name': "более 6 лет"}
        }

        experience = user_params['experience']
        if experience.isdigit():
            for key in dict_experience.keys():
                if int(experience) in key:
                    user_params['experience'] = dict_experience[key]['id']
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
    def get_params_vacancy(job_item: dict) -> dict:
        """
        Метод получающий параметры вакансии и возвращающий словарь
        :param job_item: json словарь полученный от API с вакансией
        :return: возвращает словарь с вакансией
        """
        id_vacancy = int(job_item['id'])
        name = job_item['name']
        if job_item['salary']:
            currency = 'BYN' if job_item['salary']['currency'].upper() == 'BYR' else job_item['salary']['currency'].upper()
            salary = {'from': job_item['salary']['from'],
                      'to': job_item['salary']['to'],
                      'currency': currency}
        else:
            salary = None
        experience = job_item.get('experience').get('name')
        requirement = job_item.get('snippet').get('requirement')
        responsibility = job_item.get('snippet').get('responsibility')
        description = f"{requirement if requirement else ''} {responsibility if responsibility else ''}"
        area = job_item.get('area').get('name')
        employer = {
            'name': job_item.get('employer').get('name'),
            'alternate_url': job_item.get('employer').get('alternate_url')
        }
        alternate_url = job_item.get('alternate_url')
        data = {'id': id_vacancy,
                'name': name,
                'salary': salary,
                'experience': experience,
                'description': description,
                'area': area,
                'employer': employer,
                'url_vacancy': alternate_url,
                'platform': 'HeadHunter'}
        return data

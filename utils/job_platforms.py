from abc import ABC, abstractmethod
import requests
from utils.exceptions import ResponseError
import random
import time


class JobVacancyAPI(ABC):

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass


class HeadHunterAPI(JobVacancyAPI):

    url = 'https://api.hh.ru/vacancies/'

    def __init__(self):
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

    def get_vacancies(self, **kwargs):
        data = self.correct_query(kwargs)
        self.params['text'] = data['search_query']
        self.params['only_with_salary'] = data['salary']
        if data.get('experience'):
            self.params['experience'] = data['experience']
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers)
            if response.status_code == 200:
                resp = response.json()
                found = resp['found']
                pages = resp['pages']
                index = 0
                for page_num in range(pages):
                    page = resp['page']
                    for job in resp['items']:
                        index += 1
                        job_vacancy = self.get_params_vacancy(job, index)
                        print(job_vacancy)
                    if page < pages:
                        self.params['page'] = self.params.get('page') + 1
                        resp = self.get_page_vacancy()

                print(f'Всего вакансий: {found}')

        except ResponseError as ex:
            print(ex)

    def get_page_vacancy(self):
        random_time = random.uniform(0.2, 0.4)
        time.sleep(random_time)
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data

    @staticmethod
    def correct_query(value):

        dict_experience = {
            range(0, 1): 'noExperience',
            range(1, 3): 'between1And3',
            range(3, 6): 'between3And6',
            range(6, 100): 'moreThan6'
        }

        experience = value['experience']
        if experience.strip().isdigit():
            for key in dict_experience.keys():
                if int(experience) in key:
                    value['experience'] = dict_experience[key]
        else:
            del value['experience']

        salary = value['salary']
        if salary.isdigit():
            salary = int(salary)
            data = True if salary == 1 else False
        else:
            data = False
        value['salary'] = data

        return value

    @staticmethod
    def get_params_vacancy(job_item, index):
        name = job_item['name']
        if job_item['salary']:
            salary = {'from': job_item['salary']['from'],
                      'to': job_item['salary']['to'],
                      'currency': job_item['salary']['currency']}
        else:
            salary = None
        experience = job_item['experience']['name']
        alternate_url = job_item['alternate_url']
        data = {'id': index,
                'name': name,
                'salary': salary,
                'experience': experience,
                'url_vacancy': alternate_url}
        return data


class SuperJobAPI(JobVacancyAPI):
    def get_vacancies(self, **kwargs):
        pass
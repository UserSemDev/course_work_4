from src.mixins import MixinExchanges


class Vacancy(MixinExchanges):

    def __init__(self, **kwargs: dict) -> None:
        """Инициализация параметров вакансии"""
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.salary = kwargs['salary']
        if self.salary is None:
            self.from_salary = 0
            self.to_salary = 0
        else:
            self.from_salary = self.salary.get('from')
            self.to_salary = self.salary.get('to')
        if self.salary['currency'] != 'руб.':
            self.convert_salary()
        self.experience = kwargs['experience']
        self.description = kwargs['description']
        self.area = kwargs['area']
        self.employer = kwargs['employer']
        self.url_vacancy = kwargs['url_vacancy']
        self.platform = kwargs['platform']
        self.__value = 0

    def __str__(self) -> str:
        """
        Магический метод отображения вакансии для пользователя
        :return: возвращает строку с вакансией
        """
        if self.salary:
            if self.from_salary and self.to_salary:
                salary = f"{self.from_salary}-{self.to_salary} {self.salary['currency']}"
            elif self.from_salary and not self.to_salary:
                salary = f"от {self.from_salary} {self.salary['currency']}"
            elif not self.from_salary and self.to_salary:
                salary = f"до {self.to_salary} {self.salary['currency']}"
            else:
                salary = "не указана"
        else:
            salary = "не указана"
        return (f"Вакансия: {self.name} | Зарплата: {salary} | Опыт работы: {self.experience} | "
                f"Город: {self.area} | URL вакансии: {self.url_vacancy}")

    def __repr__(self) -> str:
        """
        Магический метод отображения вакансии для разработчика
        :return: возвращает строку с вакансией
        """
        data = (f"Экземпляр класса: {self.__class__.__name__}\n"
                f"Аргументы: {self.id=}, {self.name=}, {self.salary=}, {self.experience=}, {self.description=}, "
                f"{self.area=}, {self.employer=}, {self.url_vacancy=}, {self.platform=}")
        return data

    @property
    def value(self) -> int:
        """
        Геттер для получения зарплаты
        :return: возвращает зарплату
        """
        if self.from_salary and self.to_salary:
            self.__value = (self.from_salary + self.to_salary) // 2
        elif self.from_salary and not self.to_salary:
            self.__value = self.from_salary
        elif not self.from_salary and self.to_salary:
            self.__value = self.to_salary
        return self.__value

    def __lt__(self, other) -> bool:
        """
        Магический метод сравнения вакансий
        :param other: вакансия для сравнения
        :return: возвращает результат сравнения
        """
        return self.value < other.value

    def convert_salary(self) -> None:
        """
        Метод конвертации валюты вакансии в рубли
        :return: None
        """
        rates = MixinExchanges.get_exchanges_rates()
        if not (rates == -1):
            if self.salary:
                cur_s = self.salary['currency']
                if cur_s != 'RUR':
                    from_s = self.from_salary
                    to_s = self.to_salary
                    if from_s:
                        for rate in rates:
                            if cur_s in rate['code']:
                                self.from_salary = round(from_s / rate['units'] * rate['course'])
                                self.salary['from'] = self.from_salary
                    else:
                        self.from_salary = 0
                        self.salary['from'] = 0
                    if to_s:
                        for rate in rates:
                            if cur_s in rate['code']:
                                self.to_salary = round(to_s / rate['units'] * rate['course'])
                                self.salary['to'] = self.to_salary
                    else:
                        self.to_salary = 0
                        self.salary['to'] = 0

                self.salary['currency'] = 'руб.'

            else:
                self.from_salary = 0
                self.to_salary = 0

    def correct_info_vacancy(self) -> dict:
        """
        Метод формирующий словарь вакансии
        :return: возвращает словарь вакансии
        """
        data = {
            'id': self.id,
            'name': self.name,
            'salary': self.salary,
            'experience': self.experience,
            'description': self.description,
            'area': self.area,
            'employer': self.employer,
            'url_vacancy': self.url_vacancy,
            'platform': self.platform
        }

        return data

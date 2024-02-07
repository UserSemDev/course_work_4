import json
import os
from abc import ABC, abstractmethod

from config import VACANCY_ALL_JSON_PATH


class BaseSaver(ABC):
    """Абстрактный класс сохранения"""

    @abstractmethod
    def add_vacancy(self, vacancy) -> None:
        """
        Абстрактный метод добавления вакансии
        :param vacancy: экземпляр вакансии
        :return: None
        """
        pass

    def del_vacancy(self, vacancy) -> None:
        """
        Абстрактный метод удаления вакансии
        :param vacancy: экземпляр вакансии
        :return: None
        """
        pass


class JSONSaver(BaseSaver):
    """Класс сохранения в json файл"""

    def __init__(self):
        """Инициализация параметров"""
        self.file_path = VACANCY_ALL_JSON_PATH

    def add_vacancy(self, vacancy_obj) -> None:
        """
        Метод добавления вакансии в json файл
        :param vacancy_obj: экземпляр вакансии для добавления
        :return: None
        """
        data_json = vacancy_obj.correct_info_vacancy()
        with open(self.file_path, "a", encoding='UTF-8') as f:
            if os.stat(self.file_path).st_size == 0:
                json.dump([data_json], f, indent=2, ensure_ascii=False)
            else:
                with open(self.file_path, encoding='UTF-8') as file:
                    data_vacancy = json.load(file)
                data_vacancy.append(data_json)
                with open(self.file_path, "w", encoding='UTF-8') as outfile:
                    json.dump(data_vacancy, outfile, indent=2, ensure_ascii=False)

    def del_vacancy(self, vacancy_obj) -> None:
        """
        Метод удаления вакансии из json файла
        :param vacancy_obj: экземпляр вакансии для удаления
        :return: None
        """
        data_json = vacancy_obj.correct_info_vacancy()
        with open(self.file_path, encoding='UTF-8') as file:
            data_vacancy = json.load(file)
        if data_json in data_vacancy:
            for item in data_vacancy:
                if item == data_json:
                    index = data_vacancy.index(item)
                    del data_vacancy[index]
                    print("Вакансия найдена. Удаляем...")
                    break
            with open(self.file_path, "w", encoding='UTF-8') as outfile:
                json.dump(data_vacancy, outfile, indent=2, ensure_ascii=False)

        else:
            print("Такой вакансии нет")

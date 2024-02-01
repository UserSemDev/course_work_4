import json
import os
from config import VACANCY_JSON_PATH


class JSONSaver:

    def add_vacancy(self, vacancy_obj):
        data_json = vacancy_obj.__dict__
        with open(VACANCY_JSON_PATH, "a", encoding='UTF-8') as f:
            if os.stat(VACANCY_JSON_PATH).st_size == 0:
                json.dump([data_json], f, indent=2, ensure_ascii=False)
            else:
                with open(VACANCY_JSON_PATH, encoding='UTF-8') as file:
                    data_vacancy = json.load(file)
                data_vacancy.append(data_json)
                with open(VACANCY_JSON_PATH, "w", encoding='UTF-8') as outfile:
                    json.dump(data_vacancy, outfile, indent=2, ensure_ascii=False)

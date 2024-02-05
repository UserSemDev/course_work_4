import requests
from bs4 import BeautifulSoup
from utils.exceptions import ResponseError


class MixinExchanges:

    _exchanges_rates = None

    @staticmethod
    def get_exchanges_rates():

        if MixinExchanges._exchanges_rates is None:

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36',
            }

            response = requests.get('https://www.cbr.ru/currency_base/daily/', headers=headers)
            if response.status_code != 200:
                raise ResponseError(f'Ошибка запроса, статус код {response.status_code}')
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_currency = soup.find('div', class_='table-wrapper').find_all('tr')
                exchange = []
                for currency in all_currency[1:]:
                    data = currency.find_all('td')
                    money = {'code': data[1].text,
                             'units': int(data[2].text),
                             'course': float(data[4].text.replace(',', '.')),
                             'name': data[3].text
                             }
                    exchange.append(money)
                MixinExchanges._exchanges_rates = exchange

        return MixinExchanges._exchanges_rates

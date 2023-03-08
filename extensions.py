import json
import requests

from config import TOKEN, keys

class APIException(Exception):
    pass

class CryptoConverter: #@staticmethod ошибки
    @staticmethod
    def convert(amount: str, quote: str, base: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Валюты <{quote}> нет в списке: /values.\n')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Валюты <{base}> нет в списке: /values.\n')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Некорректно указана сумма <{amount}>.\n')

        if quote == base:
            raise ConvertException(f'Невозможно конвертировать в ту же валюту {base}. \n')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)

        return total_base
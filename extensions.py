import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            return APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f"Невозможно перевести сдинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}!")

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key=37b84f0f81855280a361d21578bac755"
                         f"&base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message

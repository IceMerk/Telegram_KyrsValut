import json
import requests
from config import valuta


class APIException(Exception):
    pass


class Converted:
    @staticmethod
    def chek_valuta(kurs: str) -> str or False:  # Сверяем запросы валют и присваеваем правильное значение
        for key, val in valuta.items():
            for x in val:
                if kurs[:3] in x:  # Сверяем по первым 3 символам, поэтому ошибки допустимы
                    return key
        raise KeyError

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> str:
        if base == quote:
            raise APIException('❗ Нельзя переводить одну и туже валюту ❗')

        try:
            base_val = Converted.chek_valuta(base)
        except KeyError:
            raise APIException(f'Праверь правильность написания валюты 👉 {base}')
        try:
            quote_val = Converted.chek_valuta(quote)
        except KeyError:
            raise APIException(f'Праверь правильность написания валюты 👉 {quote}')

        try:
            amount_float = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Проверь цифру 👉 {amount}')

        url = f"https://api.apilayer.com/currency_data/convert?to={quote_val}&from={base_val}&amount={amount_float}"
        payload = {}
        headers = {"apikey": "Pp4d5VYlmZo0YAtpUhoc1uc3WD4DG1re"}

        response = requests.get(url, headers=headers, data=payload)
        result = json.loads(response.text)

        return f'{amount} {base} = {result["result"]} {quote}'

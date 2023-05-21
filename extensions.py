import requests
import json
from config import keys


class ConvertionExceptions(Exception):
    pass

class CurrencyConvertion:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExceptions(f'Невозможно перевести валюту в саму себя {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExceptions(f'Не правлиьно ведена валюта {quote}\n Будьте внимательны, для ввода значений'
                                       ' переведите клавиатуру в режим ввода'
                                       ' руской клавиатуры,\n'
                                       'валюту вводите вводите только в единственном числе, как они указаны в спсике доступных валют')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExceptions(f'Не правлиьно ведена валюта {base}\n Будьте внимательны, для ввода значений'
                                       ' переведите клавиатуру в режим ввода'
                                       ' руской клавиатуры,\n'
                                       'валюту вводите вводите только в единственном числе, как они указаны в спсике доступных валют')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExceptions(
                f'Не правлиьно ведена сумма валюты {amount}\n Будьте внимательны, для ввода значений '
                'суммы используйте только цифры')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        n_base = json.loads(r.content)[keys[base]]
        return n_base

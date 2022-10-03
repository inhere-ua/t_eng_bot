"""
ЗАДАЧА!
Есть работающая программа. В ней объявлены 2 функции: get_currency_price,
которая получает на вход название криптовалюты (например: BTC) и делает
запрос к API криптобиржи Kucoin. В ответ функция возвращает текущую цену на бирже.
За один запрос она может получить цену только одной криптовалюты.
Вторая функция crypto_prices получает на вход список из названий криптовалют
(например: ['BTC', 'ETH', 'LTC']) и в цикле последовательно получает цену каждой криптовалюты
после чего добавляет название и цену в словарь.
В результате работы функция возвращает словарь из криптовалют и их актуальных цен.
Пример результата:
{'BTC': 20000, 'ETH': 1500, 'LTC': 51}
Также в программе объявлен класс-декоратор SpeedTest для измерения времени работы фукнции.
Его менять не нужно.
Программа хорошо работает и выдаёт результат.
НО заказчик обратился к нам с проблемой:
Функция работает недостаточно быстро. Вся проблема в том, что мы последовательно
отправляем запросы к API Kucoin.
Ваша задача как разработчика придумать решение, чтобы ускорить работу этого кода.
Для начала рекомендуется изучить что такое многопоточность в python и как она работает,
после этого попробовать реализовать многопоточную отправку запросов к API биржи.
"""
import requests
import time
from threading import Thread


# creating subclass of Thread to get the returned value in join() method
class ThreadReturnValue(Thread):

    # initiating default parameters
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    # run the target function
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    # tuning join method to do "return" from called function
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


# ЭТОТ КЛАСС НЕ ТРОГАТЬ! Это простейший декоратор для измерения времени работы.
class SpeedTest:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.time()
        res = self.func(*args, **kwargs)
        end = time.time()
        print(f'Time speed: {end - start} sec.')
        return res


API_URL = 'https://api.kucoin.com/api/v1/'


# Эту функцию не менять!
def get_currency_price(currency):
    url = f'{API_URL}market/stats?symbol={currency}-USDT'
    res = requests.get(url)
    data = res.json()
    return data['data']['buy']


# Внутри этой функции реализовать многопточную отправку запросов к API Kucoin.
@SpeedTest
def crypto_prices(currencies_list):
    res = {}

    # initializing empty list of the threads objects to run
    price_list = []

    for currency in currencies_list:

        # initialize thread for each currency in currencies
        price_thr = ThreadReturnValue(target=get_currency_price,
                                      args=(currency, ), name=currency)

        # add thread to the threads list
        price_list.append(price_thr)

        # run current thread
        price_thr.start()

    # get currency and price data from every run thread
    for thread in price_list:
        res[thread.name] = thread.join()

    return res


currencies = ['BTC', 'ETH', 'LTC', 'SOL']
print(crypto_prices(currencies))

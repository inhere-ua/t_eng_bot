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
import threading

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
# def crypto_prices(currencies):
#     pool = Pool(20)
#     res = pool.map(get_currency_price, currencies)
#     pool.close()
#     pool.join()
#     return res

def crypto_prices(currencies):
    res = {}
    for currency in currencies:
        price = get_currency_price(currency)
        res[currency] = price
    return res


currencies = ['BTC', 'ETH', 'LTC', 'SOL']
print(crypto_prices(currencies))



import threading
import time

# def get_data(data):
#     while True:
#         print(f"[{threading.current_thread().name}] - {data}")
#         time.sleep(5)
#
#
# # threading.Thread(target=get_data(), args=(str(time.time())),).start()
#
# thr = threading.Thread(target=get_data, args=(str(time.time()),), name="thr-1")
# thr.start()
#
# for i in range(100):
#     print(f"current {i}")
#     time.sleep(1)
#
#     if i % 10 == 0:
#         print("active thread: ", threading.active_count())
#         print("enumerate:", threading.enumerate())
#         print("thr-1 is alive:", thr.is_alive())

def get_data2(data, value):
    for _ in range(value):
        print(f"[{threading.current_thread().name}] - {data}")
        time.sleep(1)

thr_list = []

# initialize several threadings
for i in range(3):
    thr = threading.Thread(target=get_data2, args=(str(time.time()), i),
                           name=f"thr-{i}")
    thr_list.append(thr)
    thr.start()

# now let's run multiple threadings
for i in thr_list:
    i.join()

print("finish")
"""Модуль функций для antispam"""

from .tid import load_token, load_orgID
from .whois import check_request
from yandex_360 import ya360, antispam

def load_whitelist():
    '''Функция вывода содержимого белого списка'''

    __token__ = load_token()
    __orgID__ = load_orgID()
    
    return check_request(antispam.show_whitelist(__token__, __orgID__))


def show_whitelist():
    '''Функция вывода содержимого белого списка'''

    print(load_whitelist())


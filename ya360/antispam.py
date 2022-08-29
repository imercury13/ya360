"""Модуль функций для antispam"""

from .tid import load_token, load_orgID
from .whois import check_request
from yandex_360 import antispam

def load_whitelist():
    '''Функция вывода содержимого белого списка'''

    __token__ = load_token()
    __orgID__ = load_orgID()
    
    return check_request(antispam.show_whitelist(__token__, __orgID__)['allowList'])


def show_whitelist():
    '''Функция вывода содержимого белого списка'''

    print('Белый список:')
    for el in load_whitelist():
        print(el)

def add_in_whitelist(args):
    '''Функция добавление элемента в белый список'''

    wl = load_whitelist()
    wl.append(args.ipcidr)
    body = {'allowList':wl}

    __token__ = load_token()
    __orgID__ = load_orgID()

    check_request(antispam.create_whitelist(__token__, __orgID__, body))

    print('Добавлено')
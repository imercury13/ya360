"""Модуль функций для antispam"""

from yandex_360 import antispam
from .tid import load_token, load_orgid
from .tools import check_request


def load_whitelist():
    '''Функция вывода содержимого белого списка'''

    __token__ = load_token()
    __orgid__ = load_orgid()
    
    return check_request(antispam.show_whitelist(__token__, __orgid__)['allowList'])


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
    __orgid__ = load_orgid()

    check_request(antispam.create_whitelist(__token__, __orgid__, body))

    print('Добавлено')


def delete_whitelist():
    '''Функция удаления всего белого списка'''

    __token__ = load_token()
    __orgid__ = load_orgid()

    check_request(antispam.delete_whitelist(__token__, __orgid__))


def remove_from_whitelist(args):
    '''Функция удаления элемента из белого списка'''

    wl = load_whitelist()
    try:
        wl.remove(args.ipcidr)
    except:
        print('Элемент не найден в списке')
        exit(1)

    if len(wl)>0:
        body = {'allowList':wl}

        __token__ = load_token()
        __orgid__ = load_orgid()

        check_request(antispam.create_whitelist(__token__, __orgid__, body))

    else:
        delete_whitelist()

    print('Удалено')

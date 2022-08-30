"""Модуль функций для routing"""

from .tid import load_token, load_orgID
from .tools import check_request
from yandex_360 import routing
import json


def load_routing():
    '''Функция загрузки содержимого таблицы правил'''

    __token__ = load_token()
    __orgID__ = load_orgID()

    return check_request(routing.show_routing(__token__, __orgID__)['rules'])

def show_routing():
    '''Функция вывода содержимого таблицы правил'''

    print('Правила:')
    i=1
    for el in load_routing():
        print(f'{"":8} {i:>3} {el}')
        i+=1

def add_in_routing(args):
    '''Функция добавление правила в таблицу'''
    rt = load_routing()
    
    if args.pos:
        rt.insert(args.pos, json.loads(args.rule))
    else:
        rt.append(args.rule)
    
    body = {'rules':rt}

    __token__ = load_token()
    __orgID__ = load_orgID()

    check_request(routing.edit_routing(__token__, __orgID__, body))

    print('Добавлено')
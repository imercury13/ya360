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
        print(f'{"":5} {i:>3} {json.dumps(el)}')
        i+=1

def add_in_routing(args):
    '''Функция добавление правила в таблицу'''
    rt = load_routing()
    
    if args.position:
        rt.insert(args.position, json.loads(args.rule))
    else:
        rt.append(json.loads(args.rule))
    
    body = {'rules':rt}

    __token__ = load_token()
    __orgID__ = load_orgID()

    check_request(routing.edit_routing(__token__, __orgID__, body))

    print('Добавлено')

def remove_from_routing(args):
    '''Функция удаления правила из таблицы'''

    rt = load_routing()

    try:
        rt.pop(args.position-1)
    except:
        print('Неверный номер правила')
        exit(1)
    
    body = {'rules':rt}

    __token__ = load_token()
    __orgID__ = load_orgID()

    check_request(routing.edit_routing(__token__, __orgID__, body))

    print('Удалено')
"""Модуль функций работы с API Yandex 360 журналми диска и почты"""

import csv
from pprint import pprint
from yandex_360 import tools
from .tid import load_token, load_orgid
from .tools import check_request, nickname_to_uid, check_types

def show_mail_log(args):
    """Функция возвращает список событий в аудит-логе Почты организации
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    beforeDate=None
    afterDate=None
    includeUids=None
    excludeUids=None
    types=None

    if args.includeUsers:
        includeUids = nickname_to_uid(__token__,__orgid__, args.includeUsers.split(','))

    if args.excludeUsers:
        excludeUids = nickname_to_uid(__token__,__orgid__, args.excludeUsers.split(','))

    if args.beforeDate:
        beforeDate = args.beforeDate

    if args.afterDate:
        afterDate = args.afterDate

    if args.types:
        types = args.types.split(',')
        check_types(types)

    res = check_request(tools.get_mail_log(__token__,__orgid__,beforeDate,afterDate,includeUids,excludeUids,types))['events']

    if args.csv:
        with open(args.csv, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(res[0].keys())
            for ln in res:
                writer.writerow(ln.values())
    else:
        pprint(res)

    return None

def show_disk_log(args):
    """Функция возвращает список событий в аудит-логе Диска организации
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    beforeDate=None
    afterDate=None
    includeUids=None
    excludeUids=None

    if args.includeUsers:
        includeUids = nickname_to_uid(__token__,__orgid__, args.includeUsers.split(','))

    if args.excludeUsers:
        excludeUids = nickname_to_uid(__token__,__orgid__, args.excludeUsers.split(','))

    if args.beforeDate:
        beforeDate = args.beforeDate

    if args.afterDate:
        afterDate = args.afterDate

    res = check_request(tools.get_disk_log(__token__,__orgid__,beforeDate,afterDate,includeUids,excludeUids))['events']

    if args.csv:
        with open(args.csv, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(res[0].keys())
            for ln in res:
                writer.writerow(ln.values())
    else:
        pprint(res)

    return None
"""Модуль функций работы с API Yandex 360 почтой и почтовыми ящиками"""

from yandex_360 import tools, mail, users
from .tid import load_token, load_orgid
from .tools import check_request


def edit_access_mailbox(args):
    """Функция предоставляет или изменяет права доступа сотрудника к чужому почтовому ящику
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']
    to_uid = check_request(tools.get_id_user_by_nickname(args.to_nickname, __token__, __orgid__))['id']

    rights = []

    if args.imap_full_access:
        rights.append('imap_full_access')

    if args.send_on_behalf:
        rights.append('send_on_behalf')

    if args.send_as:
        rights.append('send_as')

    if len(rights)==0:
        rights = ['imap_full_access','send_on_behalf','send_as']

    body = {"rights": rights}

    res = check_request(mail.edit_access_mailbox(__token__, __orgid__, uid, to_uid, body))

    return print(res['taskId'])


def delete_access_mailbox(args):
    """Функция удаляет все права доступа сотрудника к почтовому ящику
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']
    to_uid = check_request(tools.get_id_user_by_nickname(args.to_nickname, __token__, __orgid__))['id']

    res = check_request(mail.delete_access_mailbox(__token__, __orgid__, uid, to_uid))

    return print(res['taskId'])


def show_status_access_mailbox(args):
    """Функция возвращает статус задачи на управление правами доступа
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    res = check_request(mail.show_status_access_mailbox(__token__, __orgid__, args.taskid))

    return print(res['status'])


def show_access_mailbox_user(args):
    """Возвращает список почтовых ящиков, к которым у сотрудника есть права доступа
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

    res = check_request(mail.show_access_mailbox_user(__token__, __orgid__, uid))

    print(f'Пользователь {users.show_user(__token__,__orgid__,uid)["displayName"]} имеет доступ к ящикам:')
    for mailbox in res['resources']:
        print(f'{users.show_user(__token__,__orgid__,mailbox["resourceId"])["displayName"]}: {mailbox["rights"]}')

    return None


def show_users_access_mailbox(args):
    """Возвращает список сотрудников, у которых есть права доступа к почтовому ящику
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

    res = check_request(mail.show_users_access_mailbox(__token__, __orgid__, uid))

    print(f'К почтовому ящику {users.show_user(__token__,__orgid__,uid)["displayName"]} имеют доступ:')
    for mailbox in res['actors']:
        print(f'{users.show_user(__token__,__orgid__,mailbox["actorId"])["displayName"]}: {mailbox["rights"]}')

    return None

def show_main_address(args):
    """Возвращает почтовый адрес, с которого отправляются письма по умолчанию
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

    res = check_request(mail.show_sender_info(__token__, __orgid__, uid))

    print(f'{res["fromName"]} {res["defaultFrom"]}')

    return None


def show_signs(args):
    """Возвращает подписи и настройки
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

    res = check_request(mail.show_sender_info(__token__, __orgid__, uid))

    print(f'{res["fromName"]}\nРасположение подписи: {res["signPosition"]}')

    i=0
    print('-'*10)
    for sign in res['signs']:
        print(f'{i:<3} | По умолчанию: {str(sign["isDefault"]):<5} | Язык: {sign["lang"]:<2} | К адресам: {sign["emails"]}')
        print(f'{"":<5} Подпись:\n{sign["text"]}')
        print('-'*10)
        i+=1

    return None

def edit_main_address(args):
    """Изменяет почтовый адрес, с которого отправляются письма по умолчанию
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

    __token__ = load_token()
    __orgid__ = load_orgid()

    uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

    body = check_request(mail.show_sender_info(__token__, __orgid__, uid))

    body['defaultFrom'] = args.defaultFrom

    res = check_request(mail.edit_sender_info(__token__,__orgid__,uid,body))

    print(f'{res["fromName"]} {res["defaultFrom"]}')

    return None

"""Модуль функций для whois"""

from yandex_360 import users, departments, groups
from .tid import load_token, load_orgid
from .tools import check_request


def search_in_groups(sstr):
	"""Функция поиска групп
	
	:param sstr: строка поиска
	:type sstr: str
	:return: результат поиска
	:rtype: str
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()
	ret = {}

	grps = check_request(groups.show_groups(__token__, __orgid__))
	while grps['page'] <= grps['pages']:
		for g in grps['groups']:
			if g['label'] == sstr:
				ret.update(g)
			else:
				for a in g['aliases']:
					if a == sstr:
						ret.update(g)
		grps = groups.show_groups(__token__, __orgid__, page=grps['page']+1)

	return ret

def search_in_departments(sstr):
	"""Функция поиска поздразделений
	
	:param sstr: строка поиска
	:type sstr: str
	:returns: результат поиска
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()
	ret = {}

	dep = check_request(departments.show_departments(__token__, __orgid__))
	while dep['page'] <= dep['pages']:
		for d in dep['departments']:
			if d['label'] == sstr:
				ret.update(d)
			else:
				for a in d['aliases']:
					if a == sstr:
						ret.update(d)
		dep = departments.show_departments(__token__, __orgid__, page=dep['page']+1)

	return ret

def search_in_users(sstr):
	"""Функция поиска пользователей
	
	:param sstr: строка поиска
	:type sstr: str
	:returns: результат поиска
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()
	ret = {}
	usrs = check_request(users.show_users(__token__, __orgid__))
	while usrs['page'] <= usrs['pages']:
		for u in usrs['users']:
			if u['nickname'] == sstr:
				ret.update(u)
			else:
				for a in u['aliases']:
					if a == sstr:
						ret.update(u)
		usrs = users.show_users(__token__, __orgid__, page=usrs['page']+1)

	return ret

def whois(args):
	"""Функция поиска
	
	:param args: набор аргументов из argparse
	:type args: dict
	:returns: вывод результата поиска
	"""
	ret = {'user':{},'department':{},'group':{}}
	ret['group'] = search_in_groups(args.name)
	ret['department'] = search_in_departments(args.name)
	ret['user'] = search_in_users(args.name)
	if len(ret['group']) > 0:
		print('Найдена группа:')
		print(f'{"ID":<3s} {"Тип":<20s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<50s}')
		print(f'{ret["group"]["id"]:>3d} {ret["group"]["type"]:<20s} {ret["group"]["label"]:<15s} {ret["group"]["email"]:<30s} {ret["group"]["name"]:<50s} {ret["group"]["description"]:<50s}')
	if len(ret['department']) > 0:
		print('Найдено подразделение:')
		print(f'{"ID":<3s} {"pID":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<50s}')
		print(f'{ret["department"]["id"]:>3d} {ret["department"]["parentId"]:>3d} {ret["department"]["label"]:<15s} {ret["department"]["email"]:<30s} {ret["department"]["name"]:<50s} {ret["department"]["description"]:<50s}')
	if len(ret['user']) > 0:
		print('Найден пользователь:')
		print(f'{"ID":<17s} {"dID":<3s} {"Nickname":<25s} {"Ф.И.О.":<40s}')
		print(f'{ret["user"]["id"]:>17s} {ret["user"]["departmentId"]:>3d} {ret["user"]["nickname"]:<25s} {ret["user"]["name"]["last"]+" "+ret["user"]["name"]["first"]+" "+ret["user"]["name"]["middle"]:<40s}')
	if len(ret['group']) == 0 and len(ret['department']) == 0 and len(ret['user']) == 0:
		print('Ничего не найдено')

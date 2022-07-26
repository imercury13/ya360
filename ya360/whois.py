"""Модуль функций для whois"""
from .tid import load_token, load_orgID
from .ya import check_request
from yandex_360 import ya360

def search_in_groups(sstr):
	"""Функция поиска групп
	
	:param sstr: строка поиска
	:type sstr: str
	:return: результат поиска
	:rtype: str
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'perPage=10000'
	groups = ya360.show_groups(__token__, __orgID__, url)
	check_request(groups)
	for g in groups['groups']:
		if g['label'] == sstr:
			ret.update(g)
		else:
			for a in g['aliases']:
				if a == sstr:
					ret.update(g)
	return ret

def search_in_departments(sstr):
	"""Функция поиска поздразделений
	
	:param sstr: строка поиска
	:type sstr: str
	:returns: результат поиска
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'perPage=1000'
	departments = ya360.show_departments(__token__, __orgID__, url)
	check_request(departments)
	for d in departments['departments']:
		if d['label'] == sstr:
			ret.update(d)
		else:
			for a in d['aliases']:
				if a == sstr:
					ret.update(d)

	return ret

def search_in_users(sstr):
	"""Функция поиска пользователей
	
	:param sstr: строка поиска
	:type sstr: str
	:returns: результат поиска
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'perPage=1000'
	users = ya360.show_users(__token__, __orgID__, url)
	check_request(users)
	for u in users['users']:
		if u['nickname'] == sstr:
			ret.update(u)
		else:
			for a in u['aliases']:
				if a == sstr:
					ret.update(u)

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
		print('{0:<3s} {1:<20s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format('Id', 'Тип', 'Имя', 'E-mail', 'Название', 'Описание'))
		print('{0:>3d} {1:<20s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format(ret['group']['id'], ret['group']['type'], ret['group']['label'], ret['group']['email'], ret['group']['name'], ret['group']['description']))
	if len(ret['department']) > 0:
		print('Найдено подразделение:')
		print('{0:<3s} {1:<3s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format('Id', 'pId', 'Имя', 'E-mail', 'Название', 'Описание'))
		print('{0:>3d} {1:>3d} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format(ret['department']['id'], ret['department']['parentId'], ret['department']['label'], ret['department']['email'], ret['department']['name'], ret['department']['description']))
	if len(ret['user']) > 0:
		print('Найден пользователь:')
		print('{:<17s} {:<3s} {:<25s} {:<40s}'.format('ID','dID','Nickname','Ф.И.О.'))
		print('{:>17s} {:>3d} {:<25s} {:<40s}'.format(ret['user']['id'], ret['user']['departmentId'], ret['user']['nickname'], ret['user']['name']['last']+' '+ret['user']['name']['first']+' '+ret['user']['name']['middle']))
	if len(ret['group']) == 0 and len(ret['department']) == 0 and len(ret['user']) == 0:
		print('Ничего не найдено')

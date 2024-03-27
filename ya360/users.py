"""Модуль функций работы с API Yandex 360 пользователи"""

from .tid import load_token, load_orgID
from yandex_360 import users, tools
from .whois import search_in_users, search_in_groups, search_in_departments
from .tools import check_request
import csv

def show_users(args):
	"""Функция вывода списка всех пользователей
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	
	users = check_request(tools.get_users(__token__, __orgID__))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['ID','dID','Nickname','Ф.И.О.', 'Альясы','ID групп'])
			for member in users['users']:
				gr = " ".join(str(x) for x in member['groups'])
				al = " ".join(str(x) for x in member['aliases'])
				nm = member['name']['last']+' '+member['name']['first']+' '+member['name']['middle']
				writer.writerow([member['id'], member['departmentId'], member['nickname'], nm, al, gr])
	else:
		print(f'{"ID":<17s} {"dID":<3s} {"Nickname":<25s} {"Ф.И.О.":<40s} {"Альясы":<30s} {"ID групп":<s}')
		for member in users['users']:
			gr = " ".join(str(x) for x in member['groups'])
			al = " ".join(str(x) for x in member['aliases'])
			nm = member['name']['last']+' '+member['name']['first']+' '+member['name']['middle']
			print(f'{member["id"]:>17s} {member["departmentId"]:>3d} {member["nickname"]:<25s} {nm:<40s} {al:<30s} {gr:<}')


def show_user(args):
	"""Функция вывода информации о пользователе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']
	
	ds = check_request(users.show_user(__token__, __orgID__, ID))

	print(f'{"ID":>20s} {ds["id"]:<17s}')
	print(f'{"Nickname (Login):":>20s} {ds["nickname"]:<17s}')
	print(f'{"Ф.И.О.:":>20s} {ds["name"]["last"]+" "+ds["name"]["first"]+" "+ds["name"]["middle"]:<17s}')
	print(f'{"displayName:":>20s} {ds["displayName"]:<17s}')
	print(f'{"Должность:":>20s} {ds["position"]:<17s}')
	print(f'{"Подразделение:":>20s} {check_request(departments.show_department(__token__, __orgID__, str(ds["departmentId"])))["name"]:<17s}')
	print(f'{"E-mail:":>20s} {ds["email"]:<17s}')
	al = ", ".join(str(x) for x in ds['aliases'])
	print(f'{"Альясы:":>20s} {al:<17s}')
	if ds['isAdmin']:
		print(f'{"Администратор:":>20s} {"Да":<17s}')
	else:
		print(f'{"Администратор:":>20s} {"Нет":<17s}')
	if ds['isDismissed']:
		print(f'{"Статус сотрудника:":>20s} {"Уволен":<17s}')
	else:
		print(f'{"Статус сотрудника:":>20s} {"Действующий":<17s}')
	if ds['isEnabled']:
		print(f'{"Статус аккаунта:":>20s} {"Действующий":<17s}')
	else:
		print(f'{"Статус аккаунта:":>20s} {"Заблокирован":<17s}')
	if ds['isRobot']:
		print(f'{"Форма жизни:":>20s} {"Робот":<17s}')
	else:
		print(f'{"Форма жизни:":>20s} {"Живой человек":<17s}')
	print(f'{"Состоит в группах:":>20s} {"":<17s}')
	groups = check_request(tools.get_groups(__token__,__orgID__))['groups']
	for group in ds['groups']:
		for in_groups in groups:
			if in_groups['id'] == group:
				name = in_groups
		print(f'{"":>20} {name["name"]:s} ({name["label"]:s})')
	print(f'{"Контакты:":>20s} {"":<17s}')
	for cn in ds['contacts']:
		print(f'{"":>10} {cn["type"]:>15}: {cn["value"]}')

def update_user(args):
	"""Функция обновления информации о пользователе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	if args.name:
		body.update({'name':{}})
		try:
			body['name'].update({'last':args.name[0]})
		except:
			pass
		try:
			body['name'].update({'first':args.name[1]})
		except:
			pass
		try:
			body['name'].update({'middle':args.name[2]})
		except:
			pass
	if args.about:body.update({'about':args.about})
	if args.displayName:body.update({'displayName':args.displayName})
	if args.departmentId: body.update({'departmentId':args.departmentId})
	if args.gender:body.update({'gender':args.gender})
	if args.phone: body.update({'contacts':[{'type':'phone_extension','value':str(args.phone)}]})
	if args.language:body.update({'language':args.language})
	if args.password:body.update({'password':args.password})
	if args.position:body.update({'position':args.position})
	if args.timezone:body.update({'timezone':args.timezone})
	if args.isAdmin:
		if args.isAdmin == 'true':body.update({'isAdmin': True})
		else: body.update({'isAdmin': False})
	if args.isEnabled:
		if args.isEnabled == 'true':body.update({'isEnabled': True})
		else: body.update({'isEnabled': False})
	if args.passwordChangeRequired:
		if args.passwordChangeRequired == 'true':body.update({'passwordChangeRequired': True})
		else: body.update({'passwordChangeRequired': False})

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	check_request(users.update_user(__token__, __orgID__, body, ID))
	print('Обновлено')

def create_user(args):
	"""Функция создания пользователя
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	if args.name:
		body.update({'name':{}})
		try:
			body['name'].update({'last':args.name[0]})
		except:
			pass
		try:
			body['name'].update({'first':args.name[1]})
		except:
			pass
		try:
			body['name'].update({'middle':args.name[2]})
		except:
			pass
	if args.about:body.update({'about':args.about})
	if args.nickname:body.update({'nickname':args.nickname})
	if args.displayName:body.update({'displayName':args.displayName})
	if args.departmentId: body.update({'departmentId':args.departmentId})
	if args.gender:body.update({'gender':args.gender})
	if args.phone: body.update({'contacts':[{'type':'phone_extension','value':str(args.phone)}]})
	if args.language:body.update({'language':args.language})
	if args.password:body.update({'password':args.password})
	if args.position:body.update({'position':args.position})
	if args.timezone:body.update({'timezone':args.timezone})
	if args.isAdmin:
		if args.isAdmin == 'true':body.update({'isAdmin': True})
		else: body.update({'isAdmin': False})

	cd = check_request(users.create_user(__token__, __orgID__, body))
	print(f'Пользователь создан с ID: {cd["id"]}')

def delete_user(args):
	"""Функция удаления пользователя (необратимая операция: будет удалено всё: почта, содержимое диска)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	check_request(users.delete_user(__token__, __orgID__, ID))
	print('Пользователь удален')

def add_alias_user(args):
	"""Функция добавления альяса пользователю
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	body = {'alias': args.alias}

	check_request(users.add_alias_user(__token__, __orgID__, ID, body))
	print('Алиас добавлен')

def delete_alias_user(args):
	"""Функция удаления альяса у пользователя
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	check_request(users.delete_alias_user(__token__, __orgID__, ID, args.alias))
	print('Алиас удален')
"""Модуль функций работы с API Yandex 360 пользователи"""

import csv
import sys
from yandex_360 import users, departments, tools
from .tid import load_token, load_orgid
from .tools import check_request


def show_users(args):
	"""Функция вывода списка всех пользователей
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	us = check_request(tools.get_users(__token__, __orgid__))

	if args.csv:
		with open(args.csv, 'w', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['ID','dID','Nickname','Ф.И.О.', 'Альясы','ID групп'])
			for member in us['users']:
				gr = " ".join(str(x) for x in member['groups'])
				al = " ".join(str(x) for x in member['aliases'])
				nm = member['name']['last']+' '+member['name']['first']+' '+member['name']['middle']
				writer.writerow([member['id'], member['departmentId'], member['nickname'], nm, al, gr])
	else:
		print(f'{"ID":<17s} {"dID":<3s} {"Nickname":<25s} {"Ф.И.О.":<40s} {"Альясы":<30s} {"ID групп":<s}')
		for member in us['users']:
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
	__orgid__ = load_orgid()

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']
	a2fa = check_request(users.show_user_2fa(__token__, __orgid__, uid))['has2fa']
	ds = check_request(users.show_user(__token__, __orgid__, uid))

	print(f'{"ID":>20s} {ds["id"]:<17s}')
	print(f'{"Nickname (Login):":>20s} {ds["nickname"]:<17s}')
	print(f'{"Ф.И.О.:":>20s} {ds["name"]["last"]+" "+ds["name"]["first"]+" "+ds["name"]["middle"]:<17s}')
	print(f'{"displayName:":>20s} {ds["displayName"]:<17s}')
	print(f'{"Должность:":>20s} {ds["position"]:<17s}')
	print(f'{"Подразделение:":>20s} {check_request(departments.show_department(__token__, __orgid__, str(ds["departmentId"])))["name"]:<17s}')
	print(f'{"2FA":>20s} {a2fa}')
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
	groups = check_request(tools.get_groups(__token__,__orgid__))['groups']
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
	__orgid__ = load_orgid()
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

	if args.about:
		body.update({'about':args.about})

	if args.displayName:
		body.update({'displayName':args.displayName})

	if args.departmentId:
		body.update({'departmentId':args.departmentId})

	if args.gender:
		body.update({'gender':args.gender})

	if args.phone:
		body.update({'contacts':[{'type':'phone_extension','value':str(args.phone)}]})

	if args.language:
		body.update({'language':args.language})

	if args.password:
		body.update({'password':args.password})

	if args.position:
		body.update({'position':args.position})

	if args.timezone:
		body.update({'timezone':args.timezone})

	if args.isAdmin:
		if args.isAdmin == 'true':
			body.update({'isAdmin': True})
		else:
			body.update({'isAdmin': False})

	if args.isEnabled:
		if args.isEnabled == 'true':
			body.update({'isEnabled': True})
		else:
			body.update({'isEnabled': False})

	if args.passwordChangeRequired:
		if args.passwordChangeRequired == 'true':
			body.update({'passwordChangeRequired': True})
		else:
			body.update({'passwordChangeRequired': False})

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

	check_request(users.update_user(__token__, __orgid__, body, uid))
	print('Обновлено')


def create_user(args):
	"""Функция создания пользователя
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()
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

	if args.about:
		body.update({'about':args.about})

	if args.nickname:
		body.update({'nickname':args.nickname})

	if args.displayName:
		body.update({'displayName':args.displayName})

	if args.departmentId:
		body.update({'departmentId':args.departmentId})

	if args.gender:
		body.update({'gender':args.gender})

	if args.phone:
		body.update({'contacts':[{'type':'phone_extension','value':str(args.phone)}]})

	if args.language:
		body.update({'language':args.language})

	if args.password:
		body.update({'password':args.password})

	if args.position:
		body.update({'position':args.position})

	if args.timezone:
		body.update({'timezone':args.timezone})

	if args.isAdmin:
		if args.isAdmin == 'true':
			body.update({'isAdmin': True})
		else:
			body.update({'isAdmin': False})

	cd = check_request(users.add_user(__token__, __orgid__, body))
	print(f'Пользователь создан с ID: {cd["id"]}')


def delete_user(args):
	"""Функция удаления пользователя (необратимая операция: будет удалено всё: почта, содержимое диска)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

	check_request(users.delete_user(__token__, __orgid__, uid))
	print('Пользователь удален')


def add_alias_user(args):
	"""Функция добавления альяса пользователю
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

	body = {'alias': args.alias}

	check_request(users.add_alias_user(__token__, __orgid__, uid, body))
	print('Алиас добавлен')


def delete_alias_user(args):
	"""Функция удаления альяса у пользователя
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

	check_request(users.delete_alias_user(__token__, __orgid__, uid, args.alias))
	print('Алиас удален')


def upload_avatar_user(args):
	"""Функция загрузки портрета пользователя из файла

	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	uid = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgid__))['id']

	try:
		with open(args.filename, mode='rb') as file:
			pic = file.read()
	except FileNotFoundError:
		print('Файл не найден!')
		sys.exit(1)

	if sys.getsizeof(pic) >= 1000000:
		print('Размер файла большой! Должен быть меньше 1 МБ')
		sys.exit(1)

	res = check_request(users.upload_user_avatar(__token__, __orgid__, uid, pic))
	print(f'Портрет загружен ({res["url"]})')

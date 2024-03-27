"""Модуль функций работы с API Yandex 360 подразделения"""

from .tid import load_token, load_orgID
from yandex_360 import departments, tools
from .whois import search_in_users, search_in_groups, search_in_departments
from .tools import check_request
import csv

def create_department(args):
	"""Функция создания подразделения
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	body.update({'label':args.label, 'parentId':1})
	if args.name: body.update({'name':args.name})
	if args.headnickname: 
		users = check_request(tools.get_users(__token__, __orgID__))['users']
		for user in users:
			if user['nickname'] == args.headnickname:
				body.update({'headId':user['id']})
	if args.parentlabel: 
		departments = check_request(tools.get_departments(__token__, __orgID__))['departments']
		for dep in departments:
			if dep['label'] == args.parentlabel:
				body.update({'parentId':dep['id']})
	if args.description: body.update({'description':args.description})
	cd = check_request(departments.create_department(__token__, __orgID__, body))
	print(f'Подразделение создано с ID: {cd["id"]}')

def update_department(args):
	"""Функция обновления информации о подразделении
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}

	if args.parentlabel: 
		departments = check_request(tools.get_departments(__token__, __orgID__))['departments']
		for dep in departments:
			if dep['label'] == args.parentlabel:
				body.update({'parentId':dep['id']})

	if args.headId: 
		users = check_request(tools.get_users(__token__, __orgID__))['users']
		for user in users:
			if user['nickname'] == args.headnickname:
				body.update({'headId':user['id']})

	if args.name: body.update({'name':args.name})
	if args.description: body.update({'description':args.description})
	if args.newlabel: body.update({'label':args.newlabel})
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(departments.update_department(__token__, __orgID__, body, str(ID)))
	print('Подразделение обновлено')

def delete_department(args):
	"""Функция удаления подразделения (необратимая операция)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(departments.delete_department(__token__, __orgID__, str(ID)))
	
	print('Подразделение удалено')

def add_alias_department(args):
	"""Функция добавления альяса подразделению
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {'alias':args.alias}
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(departments.add_alias_department(__token__, __orgID__, body, str(ID)))
	print('Алиас добавлен')

def delete_alias_department(args):
	"""Функция удаления альяса у подразделения
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(departments.delete_alias_department(__token__, __orgID__, str(ID), args.alias))
	print('Алиас удален')

def show_department(args):
	"""Функция вывода информации о подразделении
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	ds = check_request(departments.show_department(__token__, __orgID__, str(ID)))
	depts = check_request(tools.get_departments(__token__, __orgID__))['departments']
	for department in depts:
		if department['id'] == ds['parentId']:
			dname = department['name']+' ('+department['label']+')'
	if ds['headId'] == '0':
		hname = 'Не назначен'
	else:
		users = check_request(tools.get_users(__token__, __orgID__))['users']
		for user in users:
			if user['id'] == ds['headId']:
				hname = f"{user['name']['last']:s} {user['name']['first']:s} {user['name']['middle']:s} ({user['nickname']})"

	print(f'{"ID:":>10s} {ds["id"]:>d}\n{"Имя":>10s} {ds["label"]:s}\n{"Название:":>10s} {ds["name"]:50s}\n{"Описание:":>10s} {ds["description"]:50s}\n{"E-mail:":>10s} {ds["email"]:50s}\n{"Ру-ль:":>10s} {hname:s}\n{"Кол-во:":>10s} {ds["membersCount"]:d}\n')
	print(f'{"В составе:":>10s} {dname:s}\n')
	print(f'{"Алиасы:":>10s} {"":100s}')
	for alias in ds['aliases']:
		print(f'{"":>10s} {alias:s}')

def show_departments(args):
	"""Функция вывода списка всех подразделений
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	departments = check_request(tools.get_departments(__token__, __orgID__))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['Id', 'pId', 'Имя', 'E-mail', 'Название', 'Описание'])
			for d in departments['departments']:
				writer.writerow([d['id'], d['parentId'], d['label'], d['email'], d['name'], d['description']])
	else:
		print(f'{"Id":<3s} {"pId":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<50s}')
		for d in departments['departments']:
			print(f'{d["id"]:>3d} {d["parentId"]:>3d} {d["label"]:<15s} {d["email"]:<30s} {d["name"]:<50s} {d["description"]:<50s}')
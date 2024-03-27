"""Модуль функций работы с API Yandex 360 группы"""

from .tid import load_token, load_orgID
from yandex_360 import groups, tools
from .whois import search_in_users, search_in_groups, search_in_departments
from .tools import check_request
import csv


def create_group(args):
	"""Функция создания группы
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	body.update({'name':args.name})
	if args.label: body.update({'label':args.label})
	if args.adminIds: body.update({'adminIds':args.adminIds})
	if args.description: body.update({'description':args.description})
	cd = check_request(groups.create_group(__token__, __orgID__, body))
	print('Группа создана с ID: '+str(cd['id']))

def update_group(args):
	"""Функция обновления информации о группе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	if args.name: body.update({'name':args.name})
	if args.newlabel: body.update({'label':args.newlabel})
	if args.adminIds: body.update({'adminIds':args.adminIds})
	if args.description: body.update({'description':args.description})
	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	check_request(groups.update_group(__token__, __orgID__, body, str(ID)))
	print('Обновлено')

def delete_group(args):
	"""Функция удаления группы
	(необратимая операция)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	check_request(groups.delete_group(__token__, __orgID__, str(ID)))
	print(f'Группа ID: {ID} удалена')

def add_member_group(args):
	"""Функция добавления участника в группу
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}
	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	ret = search_in_users(args.member)
	if 'id' in ret:
		body.update({'type':'user', 'id':ret['id']})
	ret = search_in_groups(args.member)
	if 'id' in ret:
		body.update({'type':'group', 'id':ret['id']})
	ret = search_in_departments(args.member)
	if 'id' in ret:
		body.update({'type':'department', 'id':ret['id']})
	check_request(groups.add_member_group(__token__, __orgID__, body, str(ID)))
	print('Добавлено')

def delete_member_group(args):
	"""Функция удаления участника из группы
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	ret = search_in_users(args.member)
	if 'id' in ret:
		a_type = 'user'
		a_userid = ret['id']
	ret = search_in_groups(args.member)
	if 'id' in ret:
		a_type = 'group'
		a_userid = ret['id']
	ret = search_in_departments(args.member)
	if 'id' in ret:
		a_type = 'department'
		a_userid = ret['id']
	check_request(groups.delete_member_group(__token__, __orgID__, str(ID), a_type, str(a_userid)))
	print(f'Участник {a_type}: {a_userid} удален из группы: {ID}')

def show_group(args):
	"""Функция отображения информации о группе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	grps = check_request(groups.show_group(__token__, __orgID__, str(ID)))
	print(f'{"ID:":>10s} {grps["id"]:d}\n{"Тип:":>10s} {grps["type"]:50s}\n{"Имя:":>10s} {grps["label"]:50s}\n{"Название:":>10s} {grps["name"]:50s}\n{"Описание:":>10s} {grps["description"]:50s}\n{"E-mail:":>10s} {grps["email"]:50s}\n{"Кол-во:":>10s} {grps["membersCount"]:d}\n')
	print(f'{"Участник:":>10s} {"":<100s}')
	lgroups = check_request(tools.get_groups(__token__,__orgID__,))['groups']
	for idg in grps['memberOf']:
		for lgroup in lgroups:
				if str(lgroup['id']) == str(idg):
					print(f'{"":>10s} {lgroup["name"]} ({lgroup["label"]})')
	print(f'{"Участники:":>10s} {"":100s}')
	for idu in grps['members']:
		if idu['type'] == 'user':
			users = check_request(tools.get_users(__token__,__orgID__))['users']
			for user in users:
				if user['id'] == idu['id']:
					print(f'{"":>10s} Пользователь: {user["name"]["last"]} {user["name"]["first"]} {user["name"]["middle"]} ({user["nickname"]})')
		if idu['type'] == 'group':
			for lgroup in lgroups:
				if str(lgroup['id']) == idu['id']:
					print(f'{"":>10s} Группа: {lgroup["name"]} ({lgroup["label"]})')
		if idu['type'] == 'department':
			departments = check_request(tools.get_departments(__token__,__orgID__))['departments']
			for department in departments:
				if str(department['id']) == idu['id']:
					print(f'{"":>10s} Подразделение: {department["name"]} ({department["label"]})')

def show_groups(args):
	"""Функция вывода списка всех групп
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	
	groups = check_request(tools.get_groups(__token__, __orgID__))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['Id', 'Тип', 'Имя', 'E-mail', 'Название', 'Описание'])
			for d in groups['groups']:
				writer.writerow([d['id'], d['type'], d['label'], d['email'], d['name'], d['description']])
	else:
		print(f'{"Id":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<s}')
		for d in groups['groups']:
			print(f'{d["id"]:>3d} {d["label"]:<15s} {d["email"]:<30s} {d["name"]:<50s} {d["description"]:<s}')
"""Модуль функций работы с API Yandex 360 группы"""

import csv
from yandex_360 import groups, tools
from .tid import load_token, load_orgid
from .whois import search_in_users, search_in_groups, search_in_departments
from .tools import check_request


def create_group(args):
	"""Функция создания группы
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	body = {}
	body.update({'name':args.name})

	if args.label:
		body.update({'label':args.label})

	if args.adminIds:
		body.update({'adminIds':args.adminIds})

	if args.description:
		body.update({'description':args.description})

	cd = check_request(groups.add_group(__token__, __orgid__, body))
	print('Группа создана с ID: '+str(cd['id']))


def update_group(args):
	"""Функция обновления информации о группе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	body = {}

	if args.name:
		body.update({'name':args.name})

	if args.newlabel:
		body.update({'label':args.newlabel})

	if args.adminIds:
		body.update({'adminIds':args.adminIds})

	if args.description:
		body.update({'description':args.description})

	gid = check_request(tools.get_id_group_by_label(args.label, __token__, __orgid__))['id']
	check_request(groups.update_group(__token__, __orgid__, body, str(gid)))
	print('Обновлено')


def delete_group(args):
	"""Функция удаления группы
	(необратимая операция)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	gid = check_request(tools.get_id_group_by_label(args.label, __token__, __orgid__))['id']
	check_request(groups.delete_group(__token__, __orgid__, str(gid)))
	print(f'Группа ID: {gid} удалена')


def add_member_group(args):
	"""Функция добавления участника в группу
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""

	__token__ = load_token()
	__orgid__ = load_orgid()

	body = {}
	gid = check_request(tools.get_id_group_by_label(args.label, __token__, __orgid__))['id']
	ret = search_in_users(args.member)
	if 'id' in ret:
		body.update({'type':'user', 'id':ret['id']})
	ret = search_in_groups(args.member)
	if 'id' in ret:
		body.update({'type':'group', 'id':ret['id']})
	ret = search_in_departments(args.member)
	if 'id' in ret:
		body.update({'type':'department', 'id':ret['id']})
	check_request(groups.add_member_group(__token__, __orgid__, body, str(gid)))
	print('Добавлено')


def delete_member_group(args):
	"""Функция удаления участника из группы
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	a_type, a_userid = str()
	gid = check_request(tools.get_id_group_by_label(args.label, __token__, __orgid__))['id']
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
	check_request(groups.delete_member_group(__token__, __orgid__, str(gid), a_type, str(a_userid)))
	print(f'Участник {a_type}: {a_userid} удален из группы: {gid}')


def show_group(args):
	"""Функция отображения информации о группе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	gid = check_request(tools.get_id_group_by_label(args.label, __token__, __orgid__))['id']
	grps = check_request(groups.show_group(__token__, __orgid__, str(gid)))
	print(f'{"ID:":>10s} {grps["id"]:d}\n{"Тип:":>10s} {grps["type"]:50s}\n{"Имя:":>10s} {grps["label"]:50s}\n{"Название:":>10s} {grps["name"]:50s}\n{"Описание:":>10s} {grps["description"]:50s}\n{"E-mail:":>10s} {grps["email"]:50s}\n{"Кол-во:":>10s} {grps["membersCount"]:d}\n')
	print(f'{"Участник:":>10s} {"":<100s}')
	lgroups = check_request(tools.get_groups(__token__,__orgid__,))['groups']
	for idg in grps['memberOf']:
		for lgroup in lgroups:
				if str(lgroup['id']) == str(idg):
					print(f'{"":>10s} {lgroup["name"]} ({lgroup["label"]})')
	print(f'{"Участники:":>10s} {"":100s}')
	for idu in grps['members']:
		if idu['type'] == 'user':
			users = check_request(tools.get_users(__token__,__orgid__))['users']
			for user in users:
				if user['id'] == idu['id']:
					print(f'{"":>10s} Пользователь: {user["name"]["last"]} {user["name"]["first"]} {user["name"]["middle"]} ({user["nickname"]})')
		if idu['type'] == 'group':
			for lgroup in lgroups:
				if str(lgroup['id']) == idu['id']:
					print(f'{"":>10s} Группа: {lgroup["name"]} ({lgroup["label"]})')
		if idu['type'] == 'department':
			departments = check_request(tools.get_departments(__token__,__orgid__))['departments']
			for department in departments:
				if str(department['id']) == idu['id']:
					print(f'{"":>10s} Подразделение: {department["name"]} ({department["label"]})')


def show_groups(args):
	"""Функция вывода списка всех групп
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgid__ = load_orgid()

	gs = check_request(tools.get_groups(__token__, __orgid__))

	if args.csv:
		with open(args.csv, 'w', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['Id', 'Тип', 'Имя', 'E-mail', 'Название', 'Описание'])
			for d in gs['groups']:
				writer.writerow([d['id'], d['type'], d['label'], d['email'], d['name'], d['description']])
	else:
		print(f'{"Id":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<s}')
		for d in gs['groups']:
			print(f'{d["id"]:>3d} {d["label"]:<15s} {d["email"]:<30s} {d["name"]:<50s} {d["description"]:<s}')

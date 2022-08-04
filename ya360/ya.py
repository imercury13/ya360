"""Модуль функций работы с API Yandex 360"""

from .tid import load_token, load_orgID
from yandex_360 import ya360, tools
from .whois import search_in_users, search_in_groups, search_in_departments, check_request

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
	cd = check_request(ya360.create_group(__token__, __orgID__, body))
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
	check_request(ya360.update_group(__token__, __orgID__, body, str(ID)))
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
	check_request(ya360.delete_group(__token__, __orgID__, str(ID)))
	print('Группа ID: '+str(ID)+' удалена')

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
	check_request(ya360.add_member_group(__token__, __orgID__, body, str(ID)))
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
	check_request(ya360.delete_member_group(__token__, __orgID__, str(ID), a_type, str(a_userid)))
	print(f'Участник {a_type}: {a_userid} удален из группы: {ID}')

def show_group(args):
	"""Функция отображения информации о группе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_group_by_label(args.label, __token__, __orgID__))['id']
	groups = check_request(ya360.show_group(__token__, __orgID__, str(ID)))
	print('{:>10s} {:d}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:d}\n'.format('ID:', groups['id'],'Тип:', groups['type'],'Имя:',groups['label'],'Название:',groups['name'],'Описание:', groups['description'],'E-mail:', groups['email'], 'Кол-во:', groups['membersCount']))
	print('{:>10s} {:<100s}'.format('Участник:',''))
	lgroups = check_request(ya360.show_groups(__token__,__orgID__,'perPage=1000'))['groups']
	for idg in groups['memberOf']:
		for lgroup in lgroups:
				if str(lgroup['id']) == str(idg):
					print(f'{"":>10s} {lgroup["name"]} ({lgroup["label"]})')
	print('{:>10s} {:100s}'.format('Участники:',''))
	users = check_request(ya360.show_users(__token__,__orgID__,'perPage=1000'))['users']
	#lgroups = check_request(ya360.show_groups(__token__,__orgID__,'perPage=1000'))['groups']
	departments = check_request(ya360.show_departments(__token__,__orgID__,'perPage=1000'))['departments']
	for idu in groups['members']:
		if idu['type'] == 'user':
			for user in users:
				if user['id'] == idu['id']:
					print(f'{"":>10s} {user["name"]["last"]} {user["name"]["first"]} {user["name"]["middle"]} ({user["nickname"]})')
		if idu['type'] == 'group':
			for lgroup in lgroups:
				if str(lgroup['id']) == idu['id']:
					print(f'{"":>10s} {lgroup["name"]} ({lgroup["label"]})')
		if idu['type'] == 'department':
			for department in departments:
				if str(department['id']) == idu['id']:
					print(f'{"":>10s} {department["name"]} ({department["label"]})')

def show_groups(args):
	"""Функция вывода списка всех групп
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	url = ''

	if args.page:
		url += 'page='+str(args.page)+'&'
	else:
		url += 'page=1&'

	if args.perPage:
		url += 'perPage='+str(args.perPage)+'&'
	else:
		url += 'perPage=1000'

	groups = check_request(ya360.show_groups(__token__, __orgID__, url))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['Id', 'Type', 'Label', 'E-mail', 'Name', 'Description'])
			for d in groups['groups']:
				writer.writerow([d['id'], d['type'], d['label'], d['email'], d['name'], d['description']])
	else:
		print('{0:<3s} {1:<20s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format('Id', 'Type', 'Label', 'E-mail', 'Name', 'Description'))
		for d in groups['groups']:
			print('{0:>3d} {1:<20s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format(d['id'], d['type'], d['label'], d['email'], d['name'], d['description']))


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
		users = check_request(ya360.show_users(__token__, __orgID__, 'perPage=1000'))['users']
		for user in users:
			if user['nickname'] == args.headnickname:
				body.update({'headId':user['id']})
	if args.parentlabel: 
		departments = check_request(ya360.show_departments(__token__, __orgID__, 'perPage=1000'))['departments']
		for dep in departments:
			if dep['label'] == args.parentlabel:
				body.update({'parentId':dep['id']})
	if args.description: body.update({'description':args.description})
	cd = check_request(ya360.create_department(__token__, __orgID__, body))
	print('Подразделение создано с ID: '+str(cd['id']))

def update_department(args):
	"""Функция обновления информации о подразделении
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	body = {}

	if args.parentlabel: 
		departments = check_request(ya360.show_departments(__token__, __orgID__, 'perPage=1000'))['departments']
		for dep in departments:
			if dep['label'] == args.parentlabel:
				body.update({'parentId':dep['id']})

	if args.headId: 
		users = check_request(ya360.show_users(__token__, __orgID__, 'perPage=1000'))['users']
		for user in users:
			if user['nickname'] == args.headnickname:
				body.update({'headId':user['id']})

	if args.name: body.update({'name':args.name})
	if args.description: body.update({'description':args.description})
	if args.newlabel: body.update({'label':args.newlabel})
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(ya360.update_department(__token__, __orgID__, body, str(ID)))
	print('Подразделение обновлено')

def delete_department(args):
	"""Функция удаления подразделения (необратимая операция)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(ya360.delete_department(__token__, __orgID__, str(ID)))
	
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
	check_request(ya360.add_alias_department(__token__, __orgID__, body, str(ID)))
	print('Алиас добавлен')

def delete_alias_department(args):
	"""Функция удаления альяса у подразделения
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	check_request(ya360.delete_alias_department(__token__, __orgID__, str(ID), args.alias))
	print('Алиас удален')

def show_department(args):
	"""Функция вывода информации о подразделении
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	ID = check_request(tools.get_id_department_by_label(args.label, __token__, __orgID__))['id']
	ds = check_request(ya360.show_department(__token__, __orgID__, str(ID)))
	departments = check_request(ya360.show_departments(__token__, __orgID__, 'perPage=1000'))['departments']
	for department in departments:
		if department['id'] == ds['parentId']:
			dname = department['name']+' ('+department['label']+')'
	if ds['headId'] == '0':
		hname = 'Не назначен'
	else:
		users = check_request(ya360.show_users(__token__, __orgID__, 'perPage=1000'))['users']
		for user in users:
			if user['id'] == ds['headId']:
				hname = f"{user['name']['last']:s} {user['name']['first']:s} {user['name']['middle']:s} ({user['nickname']})"

	print(f'{"ID:":>10s} {ds["id"]:>d}\n{"Имя":>10s} {ds["label"]:s}\n{"Название:":>10s} {ds["name"]:50s}\n{"Описание:":>10s} {ds["description"]:50s}\n{"E-mail:":>10s} {ds["email"]:50s}\n{"Ру-ль:":>10s} {hname:s}\n{"Кол-во:":>10s} {ds["membersCount"]:d}\n')
	print(f'{"В составе:":>10s} {dname:s}\n')
	print('{:>10s} {:100s}'.format('Алиасы:',''))
	for alias in ds['aliases']:
		print('{:>10s} {:s}'.format('',alias))

def show_departments(args):
	"""Функция вывода списка всех подразделений
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	url = ''

	if args.page:
		url += 'page='+str(args.page)+'&'
	else:
		url += 'page=1&'

	if args.perPage:
		url += 'perPage='+str(args.perPage)+'&'
	else:
		url += 'perPage=1000&'

	if args.orderBy:
		url += 'orderBy='+str(args.orderBy)+'&'

	if args.parentId:
		url += 'parentId='+str(args.parentId)+'&'

	url = url[:-1]

	departments = check_request(ya360.show_departments(__token__, __orgID__, url))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['Id', 'pId', 'Label', 'E-mail', 'Name', 'Description'])
			for d in departments['departments']:
				writer.writerow([d['id'], d['parentId'], d['label'], d['email'], d['name'], d['description']])
	else:
		print('{0:<3s} {1:<3s} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format('Id', 'pId', 'Label', 'E-mail', 'Name', 'Description'))
		for d in departments['departments']:
			print('{0:>3d} {1:>3d} {2:<15s} {3:<30s} {4:<50s} {5:<50s}'.format(d['id'], d['parentId'], d['label'], d['email'], d['name'], d['description']))

def show_users(args):
	"""Функция вывода списка всех пользователей
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()
	url = ''

	if args.page:
		url += 'page='+str(args.page)+'&'
	else:
		url += 'page=1&'

	if args.perPage:
		url += 'perPage='+str(args.perPage)+'&'
	else:
		url += 'perPage=1000&'

	url = url[:-1]

	users = check_request(ya360.show_users(__token__, __orgID__, url))

	if args.csv:
		with open(args.csv, 'w') as csvfile:
			writer = csv.writer(csvfile, dialect='excel')
			writer.writerow(['ID','dID','Nickname','Ф.И.О.', 'Альясы','ID групп'])
			for member in users['users']:
				gr = " ".join(str(x) for x in member['groups'])
				al = " ".join(str(x) for x in member['aliases'])
				writer.writerow([member['id'], member['departmentId'], member['nickname'], member['name']['last'],member['name']['first'],member['name']['middle'], al, gr])
	else:
		print('{:<17s} {:<3s} {:<25s} {:<40s} {:<30s} {:<s}'.format('ID','dID','Nickname','Ф.И.О.', 'Альясы','ID групп'))
		for member in users['users']:
			gr = " ".join(str(x) for x in member['groups'])
			al = " ".join(str(x) for x in member['aliases'])
			print('{:>17s} {:>3d} {:<25s} {:<40s} {:<30s} {:<}'.format(member['id'], member['departmentId'], member['nickname'], member['name']['last']+' '+member['name']['first']+' '+member['name']['middle'], al, gr))


def show_user(args):
	"""Функция вывода информации о пользователе
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']
	
	ds = check_request(ya360.show_user(__token__, __orgID__, ID))

	print('{:>20s} {:<17s}'.format('ID:',ds['id']))
	print('{:>20s} {:<17s}'.format('Nickname (Login):',ds['nickname']))
	print('{:>20s} {:<17s}'.format('Ф.И.О.:',ds['name']['last']+' '+ds['name']['first']+' '+ds['name']['middle']))
	print('{:>20s} {:<17s}'.format('Должность:',ds['position']))
	print('{:>20s} {:<17s}'.format('Подразделение:',ya360.show_department(__token__, __orgID__, str(ds['departmentId']))['name']))
	print('{:>20s} {:<17s}'.format('E-mail:', ds['email']))
	al = ", ".join(str(x) for x in ds['aliases'])
	print('{:>20s} {:<17s}'.format('Альясы:', al))
	if ds['isAdmin']:
		print('{:>20s} {:<17s}'.format('Администратор:', 'Да'))
	else:
		print('{:>20s} {:<17s}'.format('Администратор:', 'Нет'))
	if ds['isDismissed']:
		print('{:>20s} {:<17s}'.format('Статус сотрудника:', 'Уволен'))
	else:
		print('{:>20s} {:<17s}'.format('Статус сотрудника:', 'Действующий'))
	if ds['isEnabled']:
		print('{:>20s} {:<17s}'.format('Статус аккаунта:', 'Действующий'))
	else:
		print('{:>20s} {:<17s}'.format('Статус аккаунта:', 'Заблокирован'))
	if ds['isRobot']:
		print('{:>20s} {:<17s}'.format('Форма жизни:', 'Робот'))
	else:
		print('{:>20s} {:<17s}'.format('Форма жизни:', 'Живой человек'))
	gr = " ".join(str(x) for x in ds['groups'])
	print('{:>20s} {:<17s}'.format(' Состоит в группах:', ''))
	groups = check_request(ya360.show_groups(__token__,__orgID__,'perPage=1000'))
	groups = groups['groups']
	for group in ds['groups']:
		for in_groups in groups:
			if in_groups['id'] == group:
				name = in_groups
		print(f'{"":>20} {name["name"]:s} ({name["label"]:s})')
	print('{:>20s} {:<17s}'.format('Контакты:', ''))
	for cn in ds['contacts']:
		print('{:>20} {:>15}: {}'.format('',cn['type'],cn['value']))

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
	if args.departmentId: body.update({'departmentId':args.departmentId})
	if args.gender:body.update({'gender':args.gender})
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

	check_request(ya360.update_user(__token__, __orgID__, body, ID))
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
	if args.departmentId: body.update({'departmentId':args.departmentId})
	if args.gender:body.update({'gender':args.gender})
	if args.language:body.update({'language':args.language})
	if args.password:body.update({'password':args.password})
	if args.position:body.update({'position':args.position})
	if args.timezone:body.update({'timezone':args.timezone})
	if args.isAdmin:
		if args.isAdmin == 'true':body.update({'isAdmin': True})
		else: body.update({'isAdmin': False})

	cd = check_request(ya360.create_user(__token__, __orgID__, body))
	print('Пользователь создан с ID: '+str(cd['id']))

def delete_user(args):
	"""Функция удаления пользователе (необратимая операция: будет удалено всё: почта, содержимое диска)
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	check_request(ya360.delete_user(__token__, __orgID__, ID))
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

	check_request(ya360.add_alias_user(__token__, __orgID__, ID, body))
	print('Алиас добавлен')

def delete_alias_user(args):
	"""Функция удаления альяса у пользователя
	
	:param args: словарь аргументов командной строки
	:type args: dict
	"""
	__token__ = load_token()
	__orgID__ = load_orgID()

	ID = check_request(tools.get_id_user_by_nickname(args.nickname, __token__, __orgID__))['id']

	check_request(ya360.delete_alias_user(__token__, __orgID__, ID, args.alias))
	print('Алиас удален')

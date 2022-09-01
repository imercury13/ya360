"""Модуль функций работы с API Yandex 360"""

from .tid import load_token, load_orgID
from yandex_360 import ya360, tools
from .tools import check_request
from .whois import search_in_users, search_in_groups, search_in_departments
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
	print(f'{"ID:":>10s} {groups["id"]:d}\n{"Тип:":>10s} {groups["type"]:50s}\n{"Имя:":>10s} {groups["label"]:50s}\n{"Название:":>10s} {groups["name"]:50s}\n{"Описание:":>10s} {groups["description"]:50s}\n{"E-mail:":>10s} {groups["email"]:50s}\n{"Кол-во:":>10s} {groups["membersCount"]:d}\n')
	print(f'{"Участник:":>10s} {"":<100s}')
	lgroups = check_request(ya360.show_groups(__token__,__orgID__,'perPage=1000'))['groups']
	for idg in groups['memberOf']:
		for lgroup in lgroups:
				if str(lgroup['id']) == str(idg):
					print(f'{"":>10s} {lgroup["name"]} ({lgroup["label"]})')
	print(f'{"Участники:":>10s} {"":100s}')
	for idu in groups['members']:
		if idu['type'] == 'user':
			users = check_request(ya360.show_users(__token__,__orgID__,'perPage=1000'))['users']
			for user in users:
				if user['id'] == idu['id']:
					print(f'{"":>10s} Пользователь: {user["name"]["last"]} {user["name"]["first"]} {user["name"]["middle"]} ({user["nickname"]})')
		if idu['type'] == 'group':
			for lgroup in lgroups:
				if str(lgroup['id']) == idu['id']:
					print(f'{"":>10s} Группа: {lgroup["name"]} ({lgroup["label"]})')
		if idu['type'] == 'department':
			departments = check_request(ya360.show_departments(__token__,__orgID__,'perPage=1000'))['departments']
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
			writer.writerow(['Id', 'Тип', 'Имя', 'E-mail', 'Название', 'Описание'])
			for d in groups['groups']:
				writer.writerow([d['id'], d['type'], d['label'], d['email'], d['name'], d['description']])
	else:
		print(f'{"Id":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<s}')
		for d in groups['groups']:
			print(f'{d["id"]:>3d} {d["label"]:<15s} {d["email"]:<30s} {d["name"]:<50s} {d["description"]:<s}')


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
			writer.writerow(['Id', 'pId', 'Имя', 'E-mail', 'Название', 'Описание'])
			for d in departments['departments']:
				writer.writerow([d['id'], d['parentId'], d['label'], d['email'], d['name'], d['description']])
	else:
		print(f'{"Id":<3s} {"pId":<3s} {"Имя":<15s} {"E-mail":<30s} {"Название":<50s} {"Описание":<50s}')
		for d in departments['departments']:
			print(f'{d["id"]:>3d} {d["parentId"]:>3d} {d["label"]:<15s} {d["email"]:<30s} {d["name"]:<50s} {d["description"]:<50s}')

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
	
	ds = check_request(ya360.show_user(__token__, __orgID__, ID))

	print(f'{"ID":>20s} {ds["id"]:<17s}')
	print(f'{"Nickname (Login):":>20s} {ds["nickname"]:<17s}')
	print(f'{"Ф.И.О.:":>20s} {ds["name"]["last"]+" "+ds["name"]["first"]+" "+ds["name"]["middle"]:<17s}')
	print(f'{"Должность:":>20s} {ds["position"]:<17s}')
	print(f'{"Подразделение:":>20s} {check_request(ya360.show_department(__token__, __orgID__, str(ds["departmentId"])))["name"]:<17s}')
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
	groups = check_request(ya360.show_groups(__token__,__orgID__,'perPage=1000'))['groups']
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
	if args.phone: body.update({'contacts':[{'type':'phone_extension','value':str(args.phone)}]})
	if args.language:body.update({'language':args.language})
	if args.password:body.update({'password':args.password})
	if args.position:body.update({'position':args.position})
	if args.timezone:body.update({'timezone':args.timezone})
	if args.isAdmin:
		if args.isAdmin == 'true':body.update({'isAdmin': True})
		else: body.update({'isAdmin': False})

	cd = check_request(ya360.create_user(__token__, __orgID__, body))
	print(f'Пользователь создан с ID: {cd["id"]}')

def delete_user(args):
	"""Функция удаления пользователя (необратимая операция: будет удалено всё: почта, содержимое диска)
	
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

from .tid import load_token, load_orgID
from pprint import pprint
from .jreq import jreq

import csv

try:
	__token__ = load_token()
except Exception as e:
	print(e)

try:
	__orgID__ = load_orgID()
except Exception as e:
	print(e)

def print_tid():
	print(__token__, __orgID__)

def check_request(req):
	if 'code' in req and 'message' in req:
		print('Код ошибки: '+str(req['code'])+' Сообщение: '+req['message'])
		exit(1)

def create_group(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'
	body = {}
	body.update({'name':args.name})
	if args.label: body.update({'label':args.label})
	if args.adminIds: body.update({'adminIds':args.adminIds})
	if args.description: body.update({'description':args.description})
	if args.members: body.update({'members':args.members})
	cd = jreq('post', url, __token__, body)
	check_request(cd)
	print('Группа создана с ID: '+str(cd['id']))

def update_group(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'+str(args.ID)+'/'
	body = {}
	if args.name: body.update({'name':args.name})
	if args.label: body.update({'label':args.label})
	if args.adminIds: body.update({'adminIds':args.adminIds})
	if args.description: body.update({'description':args.description})
	if args.members: body.update({'members':args.members})
	cd = jreq('patch', url, __token__, body)
	check_request(cd)
	print('Обновлено')

def delete_group(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'+str(args.ID)+'/'
	dd = jreq('delete', url, __token__)
	check_request(dd)
	print('Группа ID: '+str(args.ID)+' удалена')

def add_member_group(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'+str(args.ID)+'/members'
	body = {}
	body.update({'id':args.userid})
	body.update({'type':args.type})
	cd = jreq('post', url, __token__, body)
	check_request(cd)
	print('Добавлено')

def show_group(args):
	if args.members:
		url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'+str(args.ID)+'/members/'
		members = jreq('get', url, __token__)
		check_request(members)
		print('Группы:')
		print('{:<4s} {:<50s}'.format('ID','Название группы'))
		for member in members['groups']:
			print('{:>4d} {:<50s}'.format(member['id'], member['name']))
		print('\nПодразделения:')
		print('{:<4s} {:<50s}'.format('ID','Название подразделения'))
		for member in members['departments']:
			print('{:>4d} {:<50s}'.format(member['id'], member['name']))
		print('\nСотрудники:')
		print('{:<17s} {:<3s} {:<10s} {:<40s} {:<50s} {:<6s}'.format('ID','dID','Nickname','Ф.И.О.','Должность','Пол'))
		for member in members['users']:
			print('{:>17s} {:>3d} {:<10s} {:<40s} {:<50s} {:<6s}'.format(member['id'], member['departmentId'], member['nickname'], member['name']['last']+' '+member['name']['first']+' '+member['name']['middle'], member['position'], member['gender']))
	else:
		url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/'+str(args.ID)+'/'
		groups = jreq('get', url, __token__)
		check_request(groups)
		print('{:>10s} {:d}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:d}\n'.format('ID:', groups['id'],'Тип:', groups['type'],'Название:',groups['name'],'Описание:', groups['description'],'E-mail:', groups['email'], 'Кол-во:', groups['membersCount']))
		print('{:>10s} {:<100s}'.format('Участник:',''))
		for idg in groups['memberOf']:
			print('{:>10} {:<d}'.format('',idg))
		print('\n')
		print('{:>10s} {:100s}'.format('Участники:',''))
		for idu in groups['members']:
			print('{:>10s} {:s} {:s}'.format('',idu['type'],idu['id']))

def show_groups(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/?'

	if args.page:
		url += 'page='+str(args.page)+'&'
	else:
		url += 'page=1&'

	if args.perPage:
		url += 'perPage='+str(args.perPage)+'&'
	else:
		url += 'perPage=1000'

	groups = jreq('get', url, __token__)

	check_request(groups)

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
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'
	body = {}
	body.update({'label':args.label, 'parentId':args.parentId})
	if args.name: body.update({'name':args.name})
	if args.headId: body.update({'headId':args.headId})
	if args.description: body.update({'description':args.description})
	cd = jreq('post', url, __token__, body)
	check_request(cd)
	print('Подразделение создано с ID: '+str(cd['id']))

def update_department(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'+str(args.ID)+'/'
	body = {}
	if args.parentId: body.update({'parentId':args.parentId})
	if args.name: body.update({'name':args.name})
	if args.headId: body.update({'headId':args.headId})
	if args.description: body.update({'description':args.description})
	ud = jreq('patch', url, __token__, body)
	check_request(ud)
	print('Подразделение ID: '+str(ud['id'])+' обновлено')
	print('{:>10s} {:d}\n{:>10s} {:d}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:s}\n{:>10s} {:d}\n'.format('ID:', ud['id'],'pID:', ud['parentId'],'Название:',ud['name'],'Описание:', ud['description'],'E-mail:', ud['email'], 'Ру-ль:', ud['headId'], 'Кол-во:', ud['membersCount']))
	print('{:>10s} {:100s}'.format('Алиасы:',''))
	for alias in ds['aliases']:
		print('{:>10s} {:s}'.format('',alias))

def delete_department(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'+str(args.ID)+'/'
	dd = jreq('delete', url, __token__)
	check_request(dd)
	print('Подразделение ID: '+str(args.ID)+' удалено')

def add_alias_department(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'+str(args.ID)+'/aliases/'
	body = {'alias':args.alias}
	ud = jreq('post', url, __token__, body)
	check_request(ud)
	print('{:>10s} {:d}\n{:>10s} {:d}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:s}\n{:>10s} {:d}\n'.format('ID:', ud['id'],'pID:', ud['parentId'],'Название:',ud['name'],'Описание:', ud['description'],'E-mail:', ud['email'], 'Ру-ль:', ud['headId'], 'Кол-во:', ud['membersCount']))
	print('{:>10s} {:100s}'.format('Алиасы:',''))
	for alias in ud['aliases']:
		print('{:>10s} {:s}'.format('',alias))

def delete_alias_department(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'+str(args.ID)+'/aliases/'+args.alias+'/'
	ud = jreq('delete', url, __token__)
	check_request(ud)
	print('Алиас удален')

def show_department(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/'+str(args.ID)+'/'
	ds = jreq('get', url, __token__)
	check_request(ds)
	print('{:>10s} {:d}\n{:>10s} {:d}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:50s}\n{:>10s} {:s}\n{:>10s} {:d}\n'.format('ID:', ds['id'],'pID:', ds['parentId'],'Название:',ds['name'],'Описание:', ds['description'],'E-mail:', ds['email'], 'Ру-ль:', ds['headId'], 'Кол-во:', ds['membersCount']))

	print('{:>10s} {:100s}'.format('Алиасы:',''))
	for alias in ds['aliases']:
		print('{:>10s} {:s}'.format('',alias))

def show_departments(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/?'

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

	departments = jreq('get', url, __token__)
	check_request(departments)

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
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/?'

	if args.page:
		url += 'page='+str(args.page)+'&'
	else:
		url += 'page=1&'

	if args.perPage:
		url += 'perPage='+str(args.perPage)+'&'
	else:
		url += 'perPage=1000&'

	url = url[:-1]

	users = jreq('get', url, __token__)
	check_request(users)


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
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/'+str(args.ID)+'/'
	ds = jreq('get', url, __token__)
	check_request(ds)

	print('{:>20s} {:<17s}'.format('ID:',ds['id']))
	print('{:>20s} {:<17s}'.format('Nickname:',ds['nickname']))
	print('{:>20s} {:<17s}'.format('Ф.И.О.:',ds['name']['last']+' '+ds['name']['first']+' '+ds['name']['middle']))
	print('{:>20s} {:<17s}'.format('Должность:',ds['position']))
	print('{:>20s} {:<17d}'.format('ID подразделения:',ds['departmentId']))
	gr = " ".join(str(x) for x in ds['groups'])
	print('{:>20s} {:<17s}'.format('ID групп:', gr))
	print('{:>20s} {:<17s}'.format('E-mail:', ds['email']))
	al = " ".join(str(x) for x in ds['aliases'])
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
	print('{:>20s} {:<17s}'.format('Контакты:', ''))
	for cn in ds['contacts']:
		print('{:>20} {:>15}: {}'.format('',cn['type'],cn['value']))

def update_user(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/'+str(args.ID)+'/'
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

	#pprint(body)
	cd = jreq('patch', url, __token__, body)
	check_request(cd)
	print('Обновлено')

def create_user(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/'
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


	#pprint(body)
	cd = jreq('post', url, __token__, body)
	check_request(cd)
	print('Пользователь создан с ID: '+str(cd['id']))

def add_alias_user(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/'+str(args.ID)+'/aliases/'
	body = {'alias':args.alias}
	ud = jreq('post', url, __token__, body)
	check_request(ud)
	print('Алиас добавлен')

def delete_alias_user(args):
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/'+str(args.ID)+'/aliases/'+args.alias+'/'
	ud = jreq('delete', url, __token__)
	check_request(ud)
	print('Алиас удален')

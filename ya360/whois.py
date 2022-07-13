from .tid import load_token, load_orgID
from .jreq import jreq
from .ya import check_request


def search_in_groups(sstr):
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/groups/?perPage=10000'
	groups = jreq('get', url, __token__)
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
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/departments/?perPage=1000'
	departments = jreq('get', url, __token__)
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
	__token__ = load_token()
	__orgID__ = load_orgID()
	ret = {}
	url = 'https://api360.yandex.net/directory/v1/org/'+__orgID__+'/users/?perPage=1000'
	users = jreq('get', url, __token__)
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

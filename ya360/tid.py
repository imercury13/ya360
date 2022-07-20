"""
Модуль работы с токеном и ID организации
"""
from . import __path__ as path
import pickle
from . import __version__
from .jreq import send_code
from pprint import pprint

def get_token(args):
	"""Функция получения токена по коду авторизации
	
	:returns: токен
	"""
	url = 'https://oauth.yandex.ru/authorize?response_type=code&client_id='+str(args.appid)+'&login_hint='+str(args.adminemail)+'&force_confirm=yes'
	print(url)
	#print(get_code(url).text)
	code = input("Введите код полученный на сайте: ")
	url = 'https://oauth.yandex.ru/token'
	body = 'grant_type=authorization_code&code='+str(code)+'&client_id='+str(args.appid)+'&client_secret='+str(args.appsec)
	print(url)
	print(send_code(url, body).text)

def load_token():
	"""Функция загрузки токена
	
	:returns: токен
	"""
	with open(path[0]+'/token.pickle','rb') as f:
		token = pickle.load(f)
	
	return token

	
def load_orgID():
	"""Функция загрузки id организации
	
	:returns: ID организации
	"""
	with open(path[0]+'/orgid.pickle','rb') as f:
		orgID = pickle.load(f)
	
	return orgID

	
def save_token(token):
	"""Функция записи токена
	
	  :param token: токен
	  :type token: str
	"""
	with open(path[0]+'/token.pickle','wb') as f:
		pickle.dump(token, f)

		
def save_orgID(orgID):
	"""Функция записи id организации
	
	:param orgID: ID организации
	:type orgID: str
	"""
	with open(path[0]+'/orgid.pickle','wb') as f:
		pickle.dump(orgID, f)
		

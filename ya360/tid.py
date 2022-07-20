"""
Модуль работы с токеном и ID организации
"""
from . import __path__ as path
import pickle
from . import __version__
from .configure import load_config

def load_token():
	"""Функция загрузки токена
	
	:returns: токен
	"""
	token = load_config()['access_token']
	
	return token

	
def load_orgID():
	"""Функция загрузки id организации
	
	:returns: ID организации
	"""
		
	orgID = load_config()['orgid']
	
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
		

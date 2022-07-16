"""
Модуль работы с токеном и ID организации
"""
from . import __path__ as path
import pickle
from . import __version__



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
	
	  :token: токен
	"""
	with open(path[0]+'/token.pickle','wb') as f:
		pickle.dump(token, f)

		
def save_orgID(orgID):
	"""Функция записи id организации
	
	:orgID: ID организации
	"""
	with open(path[0]+'/orgid.pickle','wb') as f:
		pickle.dump(orgID, f)
		

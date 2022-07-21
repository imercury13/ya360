"""
Модуль работы с токеном и ID организации
"""

from . import __path__ as path
from . import __version__
from yandex_oauth import yao

def load_token():
	"""Функция загрузки токена
	
	:returns: токен
	"""
	token = yao.load_token(path[0])['access_token']
	
	return token

	
def load_orgID():
	"""Функция загрузки id организации
	
	:returns: ID организации
	"""
		
	orgID = yao.load_token(path[0])['orgid']
	
	return orgID

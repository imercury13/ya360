"""
Модуль работы с токеном и ID организации
"""
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

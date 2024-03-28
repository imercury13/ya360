"""
Модуль работы с токеном и ID организации
"""

from yandex_oauth import yao
from . import __path__ as path
from . import __version__


def load_token():
	"""Функция загрузки токена
	
	:returns: токен
	"""
	token = yao.load_token(path[0])['access_token']

	return token


def load_orgid():
	"""Функция загрузки id организации
	
	:returns: ID организации
	"""

	orgid = yao.load_token(path[0])['orgid']

	return orgid

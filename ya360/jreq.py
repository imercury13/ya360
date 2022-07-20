"""
Модуль унификации вызовов requests к API Yandex 360
"""
import requests, json, time, random
from . import __version__

def jreq(mode, url, token, body=None, try_number=1):
	"""Функция передачи запроса в API Yandex 360

	:param mode: метод запроса (get,post,patch,delete)
	:type mode: str
	:param url: адрес запроса
	:type url: str
	:param token: токен авторизации запроса
	:type token: str
	:param body: тело запроса (если предусмотрено)
	:type body: dict
	:param try_number: номер попытки передачи запроса
	:type try_number: int
	:returns: json результат запроса
	"""
	try:
		if mode == 'post': response = requests.post(url, data=json.dumps(body), headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'get': response = requests.get(url, headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'patch': response = requests.patch(url, data=json.dumps(body), headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()
		if mode == 'delete': response = requests.delete(url, headers={'Authorization': 'OAuth '+token, 'Content-type': 'application/json'}).json()

	except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
		time.sleep(2**try_number + random.random()*0.01)
		print('Попытка: '+str(try_number+1))
		return jreq(mode, url, token, body, try_number=try_number+1)

	else:
		return response

def send_code(url, body):
	"""Функция запроса кода авторизации
	
	:param url: адрес запроса
	:type url: str
	:param body: тело запроса
	:type body: str
	:returns: url
	"""

	return requests.post(url, data=body, headers={'Host': 'oauth.yandex.ru', 'Content-type': 'application/x-www-form-urlencoded'})

'''Модуль вспомогательных функций'''

import sys

def check_request(req):
	"""Функция проверки ответа запроса
	
	:param req: результат запроса
	:type req: dict

	"""

	if req is None:
		print('Not Found')
		sys.exit(1)
	if 'code' in req and 'message' in req:
		print(f'Код ошибки: {req["code"]} Сообщение: {req["message"]}')
		sys.exit(1)

	return req

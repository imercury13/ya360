'''Модуль вспомогательных функций'''

import sys
from yandex_360 import tools

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


def nickname_to_uid(__token__,__orgid__,users_list):
	"""Функция преобразования списка nickname в список id"""

	uid_list = []
	for user in users_list:
		try:
			uid_list.append(tools.get_id_user_by_nickname(user,__token__,__orgid__)['id'])
		except:
			print(f'Пользователь {user} не найден')
			sys.exit(1)
	return uid_list

def check_types(types_list):
	"""Функция проверки типов событий с почтой"""

	types_const = [
		'mailbox_send','message_receive','message_seen',
		'message_unseen','message_forward','message_purge',
		'message_trash','message_spam','message_unspam',
		'message_move','message_copy','message_answer'
	]

	for tp in types_list:
		if tp not in types_const:
			print(f'Неизвестный тип события: {tp}')
			sys.exit(1)
	
	return None

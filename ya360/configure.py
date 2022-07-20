"""Модуль функций работы с конфигурационным файлом"""

from . import __path__ as path
import pickle
from . import __version__

def load_config():
    """Функция загрузки конфигурационного файла
    :returns: config или False, если нет кофигурационного файла
    """
    try:
        with open(path[0]+'/configuration.pickle','rb') as f:
            config = pickle.load(f)
    except:
        return False
    else:
	    return config

def save_config(config):
    """Функция сохранения конфигурационных параметров
    
    :param config: словарь конфигурационных параметров
    :type config: dict
    :retunrs: True или False
    """
    try:
        with open(path[0]+'/configuration.pickle','w') as f:
            pickle.dump(config, f)
    except:
        return False
    else:
        return True

def make_config():
    """Функция создания первичного конфигурационного файла"""
    print('\n\nПЕРВОНАЧАЛЬНАЯ КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ\n')
    print('1. Авторизуйтесь на Яндексе. Укажите логин и пароль администратора организации,\n   от имени которого будут выполняться запросы к API\n')
    print('      https://passport.yandex.ru/')
    print('\n')
    print('2. Зарегистрируйте приложение\n')
    print('      https://oauth.yandex.ru/client/new')
    print('\n   Заполните поля:')
    print('      Название сервиса: ya360')
    print('      Для какой платформы нужно приложение: Веб-сервисы')
    print('      Какие данные вам нужны: Яндекс 360 Admin API, Яндекс 360 Directory API (отметить все галочки)')
    print('      Callback URI: https://oauth.yandex.ru/verification_code')
    print('\n')
    print('3. Перейдите на страницу созданных приложений и выберете ya360\n')
    print('      https://oauth.yandex.ru/')
    print('\n')
    client_id = input('   Введите ClientID: ')
    client_secret = input('   Введите Client secret: ')
    adminemail = input('   Введите e-mail администратора организации, от имени которого будут выполняться запросы к API: ')
    url = 'https://oauth.yandex.ru/authorize?response_type=code&client_id='+str(client_id)+'&login_hint='+str(adminemail)+'&force_confirm=yes'
    print('\n4. Перейдите по следующей ссылке и получите код подтверждения\n')
    print('      '+url)
    print('\n')

    
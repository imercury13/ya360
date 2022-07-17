Установка
---------

Для производственного использования рекомендуется использовать стабильную версию релиза из репозитория pypi.

Установка из pypi производится следующей командой:

.. code-block:: console

    $ pip install ya360

Конфигурирование
----------------

.. warning::
    Данный метод конфигурирования является временнным и в последующих релизах будет изменен.

    Для обслуживания нескольких организаций, рекомендуется использовать механизм venv:

    .. code-block:: console

        $ python3 -m venv org1
        $ source org1/bin/activate
        $ (org1) pip install ya360
        $ (org1) deactivate
        $ python3 -m venv org2
        $ source org2/bin/activate
        $ (org2) pip install ya360
        $ (org2) deactivate


После успешной установки, утилиту необходимо настроить на работу с вашей организацией.

- Войдите под администратором организации https://passport.yandex.ru
- Зарегистрируйте приложение https://oauth.yandex.ru/client/new
- Заполните обязательные поля: название приложения, Платформы -> Веб-сервисы, Callback URI: `https://oauth.yandex.ru/verification_code`
- В доступах отметье все поля для Яндекс 360 Admin API и Яндекс 360 Directory API
- Нажмите “создать приложение”
- Затем пройдите по `https://oauth.yandex.ru/authorize?response_type=token&client_id=ID`, где `ID` - это идентификатор приложения, который необходимо взять в конце страницы зарегестрированного приложения. Подтвердить еще раз права и получить токен, который необходимо записать через команду:

.. code-block:: console

    $ ya360 token VaskTokenVydaniyYandeKsom

- ID организации можно увидеть на странице администрирования https://admin.yandex.ru/company-profile и записать его через команду:

.. code-block:: console

    $ ya360 org_id 00000


---
permalink: /install-and-config/
---
# Установка и настройка

### Установка

Для установки стабильного релиза рекомендуется пакет из [pypi](https://pypi.org/project/ya360/){:target="_blank"}, используя команду:

```bash
pip install ya360
```

### Настройка

- Войдите под администратором организации [passport.yandex.ru](https://passport.yandex.ru/){:target="_blank"}

- Зарегистрируйте приложение [oauth.yandex.ru/client/new](https://oauth.yandex.ru/client/new){:target="_blank"}

- Заполните обязательные поля: название приложения, Платформы -> Веб-сервисы, Callback URI: <https://oauth.yandex.ru/verification_code>

- В доступах отметье все поля для **Яндекс 360 Admin API** и **Яндекс 360 Directory API**

- Нажмите "создать приложение"

- Затем пройдите по <https://oauth.yandex.ru/authorize?response_type=token&client_id=><идентификатор приложения>, где <идентификатор приложения> необходимо взять в конце страницы зарегестрированного приложения. Подтвердить еще раз права и получить токен, который необходимо записать через команду

```bash
ya360 token VaskTokenVydaniyYandeKsom
```

- ID организации можно увидеть на странице администрирования [admin.yandex.ru/company-profile](https://admin.yandex.ru/company-profile){:target="_blank"} и записать его через команду

```bash
ya360 org_id 00000
```

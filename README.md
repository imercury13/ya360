# ya360
Утилита командной строки для управления организациями в Yandex 360

### Установка из pypi командой:
```
pip install ya360
```

### Регистрация приложения:

- Войдите под администратором организации https://passport.yandex.ru/

- Зарегистрируйте приложение https://oauth.yandex.ru/client/new

- Заполните обязательные поля: название приложения, Платформы -> Веб-сервисы, Callback URI#1: https://oauth.yandex.ru/verification_code

- В доступах отметье все поля для **Яндекс 360 Admin API** и **Яндекс 360 Directory API**

- Нажмите "создать приложение"

- Затем пройдите по https://oauth.yandex.ru/authorize?response_type=token&client_id=<идентификатор приложения>, где <идентификатор приложения> необходимо взять в конце страницы зарегестрированного приложения. Подтвердить еще раз права и получить токен, который необходимо записать через команду
```
ya360 token
```

- ID организации можно увидеть на странице администрирования https://admin.yandex.ru/company-profile и записать его через команду
```
ya360 org_id
```

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

---
permalink: /docs/
---
# Документация

Данная документация составлена по состоянию версии релиза:
```
# ya360 -v
ya360 2.2.1
```

## Вывод подсказки

Вывод общей подсказки или по конретной команде производится с помощью указания ключа **-h**
```
# ya360 -h
usage: ya360 [-h] [-v]
             {whois,user,users,group,groups,department,departments,token,org_id}
             ...

positional arguments:
  {whois,user,users,group,groups,department,departments,token,org_id}
                        sub-command help
    [whois](/docs/whois/)               Кто это?
    user                Пользователь
    users               Пользователи
    group               Группа
    groups              Группы
    department          Подразделение
    departments         Подразделения
    token               Добавить или изменить токен
    org_id              Добавить или изменить ID организации

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

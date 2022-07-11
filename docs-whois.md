---
permalink: /docs/whois/
---
# ya360 whois

Команда, позволяющая производить поиск сущностей по login или alias

## Вывод подсказки

Вывод подсказки с помощью указания ключа **-h**

```bash
ya360 whois -h
usage: ya360 whois [-h] name

positional arguments:
  name        Строка поиска

optional arguments:
  -h, --help  show this help message and exit
```

## Примеры

### Поиск по login

```bash
ya360 whois 1**3k**
Найден пользователь:
ID                dID Nickname                  Ф.И.О.                                  
 ***00000*******9   2 1**3k**                   ***** ******** ******
```

### Поиск по alias

```bash
ya360 whois sales
Найдена группа:
Id  Тип                  Имя             E-mail                         Название                                           Описание                                          
184 generic              sales           sales@*********.**             Сотрудники отдела продаж                           *****

ya360 whois it
Найдено подразделение:
Id  pId Имя             E-mail                         Название                                           Описание                                          
  2  43 it              it@*********.**                Департамент информационных технологий              Информационные технологии
```

[В оглавление](/docs/)

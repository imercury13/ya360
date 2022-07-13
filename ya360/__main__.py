"""
Модуль функций автозапуска при старте пакета
"""
from . import __version__
from .tid import save_token, save_orgID
import argparse, sys
from .ya import print_tid, create_group, delete_group, update_group, add_member_group, delete_member_group, show_group, show_groups, create_department, update_department, add_alias_department, delete_alias_department, delete_department, show_department, show_departments, show_users, show_user, update_user, create_user, add_alias_user, delete_alias_user, delete_user
from .whois import whois

def start():
    """Функция запуска приложения приема аргументов командной строки
    """
    parser = argparse.ArgumentParser(prog='ya360')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+__version__)

    subparsers = parser.add_subparsers(help='sub-command help', dest='sub_com')

    parser_whois = subparsers.add_parser('whois', help='Кто это?')


    parser_whois.add_argument('name', type=str, help='Строка поиска')


    parser_user = subparsers.add_parser('user', help='Пользователь')
    subparser_user = parser_user.add_subparsers(help='sub-command help', dest='sub_com_user')

    parser_user_comm = subparser_user.add_parser('create', help='Создать')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('departmentId', type=int, help='ID подразделения')
    parser_user_comm.add_argument('name', nargs='*', help='Фамилия Имя Отчество')
    parser_user_comm.add_argument('password', type=str, help='Пароль')
    parser_user_comm.add_argument('--about', type=str, help='Описание пользователя')
    parser_user_comm.add_argument('--birthday', type=str, help='YYYY-MM-DD')
    parser_user_comm.add_argument('--gender', type=str, help='Пол')
    parser_user_comm.add_argument('--isAdmin', choices=['true', 'false'], help='Признак администратора организации')
    parser_user_comm.add_argument('--language', type=str, help='Язык')
    parser_user_comm.add_argument('--position', type=str, help='Должность')
    parser_user_comm.add_argument('--timezone', type=str, help='Часовой пояс')

    parser_user_comm = subparser_user.add_parser('delete', help='Удалить')
    parser_user_comm.add_argument('ID', type=int, help='ID пользователя')

    parser_user_comm = subparser_user.add_parser('add-alias', help='Добавить алиас')
    parser_user_comm.add_argument('ID', type=int, help='ID пользователя')
    parser_user_comm.add_argument('alias', type=str, help='alias')

    parser_user_comm = subparser_user.add_parser('delete-alias', help='Удалить алиас')
    parser_user_comm.add_argument('ID', type=int, help='ID пользователя')
    parser_user_comm.add_argument('alias', type=str, help='alias')

    parser_user_comm = subparser_user.add_parser('show', help='Показать')
    parser_user_comm.add_argument('ID', type=int, help='ID пользователя')

    parser_user_comm = subparser_user.add_parser('update', help='Изменить')
    parser_user_comm.add_argument('ID', type=int, help='ID пользователя')
    parser_user_comm.add_argument('--name', nargs='*', help='Фамилия Имя Отчество')
    parser_user_comm.add_argument('--about', type=str, help='Описание пользователя')
    parser_user_comm.add_argument('--birthday', type=str, help='YYYY-MM-DD')
    parser_user_comm.add_argument('--departmentId', type=int, help='ID подразделения')
    parser_user_comm.add_argument('--gender', type=str, help='Пол')
    parser_user_comm.add_argument('--isAdmin', choices=['true', 'false'], help='Признак администратора организации')
    parser_user_comm.add_argument('--isEnabled', choices=['true', 'false'], help='Статус аккаунта')
    parser_user_comm.add_argument('--language', type=str, help='Язык')
    parser_user_comm.add_argument('--password', type=str, help='Пароль')
    parser_user_comm.add_argument('--passwordChangeRequired', choices=['true', 'false'], help='Обязательность изменения пароля при первом входе')
    parser_user_comm.add_argument('--position', type=str, help='Должность')
    parser_user_comm.add_argument('--timezone', type=str, help='Часовой пояс')


    parser_users = subparsers.add_parser('users', help='Пользователи')
    subparser_users = parser_users.add_subparsers(help='sub-command help', dest='sub_com_users')

    parser_users_comm = subparser_users.add_parser('show', help='Показать')
    parser_users_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_users_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_users_comm.add_argument('--csv', type=str, help='Save to CSV file')


    parser_group = subparsers.add_parser('group', help='Группа')
    subparser_group = parser_group.add_subparsers(help='sub-command help', dest='sub_com_group')

    parser_group_comm = subparser_group.add_parser('create', help='Создать')
    parser_group_comm.add_argument('--label', type=str, help='Имя группы')
    parser_group_comm.add_argument('name', type=str, help='Название группы')
    parser_group_comm.add_argument('--adminIds', type=str, help='Руководители')
    parser_group_comm.add_argument('--description', type=str, help='Описание группы')

    parser_group_comm = subparser_group.add_parser('update', help='Изменить')
    parser_group_comm.add_argument('ID', type=int, help='ID группы')
    parser_group_comm.add_argument('--label', type=str, help='Имя группы')
    parser_group_comm.add_argument('--name', type=str, help='Название группы')
    parser_group_comm.add_argument('--adminIds', type=str, help='Руководители')
    parser_group_comm.add_argument('--description', type=str, help='Описание группы')

    parser_group_comm = subparser_group.add_parser('add-member', help='Добавить участника')
    parser_group_comm.add_argument('ID', type=int, help='ID группы')
    parser_group_comm.add_argument('userid', type=str, help='ID участника')
    parser_group_comm.add_argument('type', choices=['user','group','department'], help='Тип участника')

    parser_group_comm = subparser_group.add_parser('delete-member', help='Удалить участника')
    parser_group_comm.add_argument('ID', type=int, help='ID группы')
    parser_group_comm.add_argument('userid', type=str, help='ID участника')
    parser_group_comm.add_argument('type', choices=['user','group','department'], help='Тип участника')

    parser_group_comm = subparser_group.add_parser('delete', help='Удалить')
    parser_group_comm.add_argument('ID', type=int, help='ID группы')

    parser_group_comm = subparser_group.add_parser('show', help='Показать')
    parser_group_comm.add_argument('ID', type=int, help='ID группы')
    parser_group_comm.add_argument('--members', action='store_true', help='Отобразить членов группы')


    parser_groups = subparsers.add_parser('groups', help='Группы')
    subparser_groups = parser_groups.add_subparsers(help='sub-command help', dest='sub_com_groups')

    parser_groups_comm = subparser_groups.add_parser('show', help='Показать')
    parser_groups_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_groups_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_groups_comm.add_argument('--csv', type=str, help='Save to CSV file')


    parser_department = subparsers.add_parser('department', help='Подразделение')
    subparser_department = parser_department.add_subparsers(help='sub-command help', dest='sub_com_department')

    parser_department_comm = subparser_department.add_parser('create', help='Создать')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('name', type=str, help='Название подразделения')
    parser_department_comm.add_argument('--parentId', type=int, default=1, help='ID родительского подразделения')
    parser_department_comm.add_argument('--headId', type=str, help='ID руководителя подразделения')
    parser_department_comm.add_argument('--description', type=str, help='Описание подразделения')

    parser_department_comm = subparser_department.add_parser('update', help='Изменить')
    parser_department_comm.add_argument('ID', type=int, help='ID подразделения')
    parser_department_comm.add_argument('--label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('--parentId', type=int, default=1, help='ID родительского подразделения')
    parser_department_comm.add_argument('--name', type=str, help='Название подразделения')
    parser_department_comm.add_argument('--headId', type=str, help='ID руководителя подразделения')
    parser_department_comm.add_argument('--description', type=str, help='Описание подразделения')

    parser_department_comm = subparser_department.add_parser('add-alias', help='Добавить алиас')
    parser_department_comm.add_argument('ID', type=int, help='ID подразделения')
    parser_department_comm.add_argument('alias', type=str, help='alias')

    parser_department_comm = subparser_department.add_parser('delete-alias', help='Удалить алиас')
    parser_department_comm.add_argument('ID', type=int, help='ID подразделения')
    parser_department_comm.add_argument('alias', type=str, help='alias')

    parser_department_comm = subparser_department.add_parser('delete', help='Удалить')
    parser_department_comm.add_argument('ID', type=int, help='ID подразделения')
    parser_department_comm = subparser_department.add_parser('show', help='Показать')
    parser_department_comm.add_argument('ID', type=int, help='ID подразделения')


    parser_departments = subparsers.add_parser('departments', help='Подразделения')
    subparser_departments = parser_departments.add_subparsers(help='sub-command help', dest='sub_com_departments')

    parser_departments_comm = subparser_departments.add_parser('show', help='Показать')
    parser_departments_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_departments_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_departments_comm.add_argument('--parentId', type=int, help='Идентификатор родителя')
    parser_departments_comm.add_argument('--orderBy', choices=['id','name'], help='Сортировать по')
    parser_departments_comm.add_argument('--csv', type=str, help='Save to CSV file')


    parser_token = subparsers.add_parser('token', help='Добавить или изменить токен')
    parser_token.add_argument('KEY', type=str, help='токен')
    parser_org_ID = subparsers.add_parser('org_id', help='Добавить или изменить ID организации')
    parser_org_ID.add_argument('orgID', type=str, help='ID организации')

    args = parser.parse_args()


    if args.sub_com == None:
        parser.print_help()

    if args.sub_com == 'whois':
        whois(args)

    if args.sub_com == 'group':
        if args.sub_com_group == 'show':
            show_group(args)
        if args.sub_com_group == 'create':
            create_group(args)
        if args.sub_com_group == 'delete':
            delete_group(args)
        if args.sub_com_group == 'add-member':
            add_member_group(args)
        if args.sub_com_group == 'delete-member':
            delete_member_group(args)
        if args.sub_com_group == 'update':
            update_group(args)

    if args.sub_com == 'groups':
        if args.sub_com_groups == 'show':
            show_groups(args)

    if args.sub_com == 'department':
        if args.sub_com_department == 'show':
            show_department(args)
        if args.sub_com_department == 'create':
            create_department(args)
        if args.sub_com_department == 'update':
            update_department(args)
        if args.sub_com_department == 'add-alias':
            add_alias_department(args)
        if args.sub_com_department == 'delete-alias':
            delete_alias_department(args)
        if args.sub_com_department == 'delete':
            delete_department(args)

    if args.sub_com == 'departments':
        if args.sub_com_departments == 'show':
            show_departments(args)

    if args.sub_com == 'users':
        if args.sub_com_users == 'show':
            show_users(args)

    if args.sub_com == 'user':
        if args.sub_com_user == 'show':
            show_user(args)
        if args.sub_com_user == 'create':
            create_user(args)
        if args.sub_com_user == 'delete':
            delete_user(args)
        if args.sub_com_user == 'update':
            update_user(args)
        if args.sub_com_user == 'add-alias':
            add_alias_user(args)
        if args.sub_com_user == 'delete-alias':
            delete_alias_user(args)

    if args.sub_com == 'token':
        try:
            save_token(args.KEY)
        except Exception as e:
            print(e)
            exit(1)
        print('Токен добавлен, либо изменен')

    if args.sub_com == 'org_id':
        try:
            save_orgID(args.orgID)
        except Exception as e:
            print(e)
            exit(1)
        print('ID добавлен, либо изменен')


if __name__ == '__main__':
    start()

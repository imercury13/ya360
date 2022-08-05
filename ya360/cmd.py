"""
Модуль командной строки
"""

from . import __version__
from . import __path__ as path
import argparse
from .ya import create_group, delete_group, update_group, add_member_group, delete_member_group, show_group, show_groups, create_department, update_department, add_alias_department, delete_alias_department, delete_department, show_department, show_departments, show_users, show_user, update_user, create_user, add_alias_user, delete_alias_user, delete_user
from .whois import whois
from .configure import make_config
from yandex_oauth import yao
import datetime

def gen_parser():
    """Функция запуска приложения приема аргументов командной строки
    """
    parser = argparse.ArgumentParser(prog='ya360')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__)

    subparsers = parser.add_subparsers(dest='sub_com')


    parser_whois = subparsers.add_parser('whois', help='Кто это?')
    parser_whois.add_argument('name', type=str, help='nickname, alias или label разыскиваемой сущности')


    parser_user = subparsers.add_parser('user', help='Действия над пользователем')
    subparser_user = parser_user.add_subparsers(help='Действия над пользователем', dest='sub_com_user')

    parser_user_comm = subparser_user.add_parser('create', help='Создать пользователя')
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

    parser_user_comm = subparser_user.add_parser('update', help='Изменить данные пользователя')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
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

    parser_user_comm = subparser_user.add_parser('delete', help='Удалить пользователя (ВНИМАНИЕ! НЕОБРАТИМАЯ ОПЕРАЦИЯ!)')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')

    parser_user_comm = subparser_user.add_parser('add-alias', help='Добавить алиас пользователю')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('alias', type=str, help='alias')

    parser_user_comm = subparser_user.add_parser('delete-alias', help='Удалить алиас у пользователя')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('alias', type=str, help='alias')

    parser_user_comm = subparser_user.add_parser('show', help='Вывести информацию о пользователе')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')

    parser_user_comm = subparser_user.add_parser('show-all', help='Вывести список пользователей')
    parser_user_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_user_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_user_comm.add_argument('--csv', type=str, help='Выгрузить в CSV файл')
    
    parser_group = subparsers.add_parser('group', help='Действия над группой')
    subparser_group = parser_group.add_subparsers(help='Действия над группой', dest='sub_com_group')

    parser_group_comm = subparser_group.add_parser('create', help='Создать группу')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')
    parser_group_comm.add_argument('name', type=str, help='Название группы')
    parser_group_comm.add_argument('--adminIds', type=str, help='Руководители')
    parser_group_comm.add_argument('--description', type=str, help='Описание группы')

    parser_group_comm = subparser_group.add_parser('update', help='Изменить группу')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')
    parser_group_comm.add_argument('--newlabel', type=str, help='Новое имя группы')
    parser_group_comm.add_argument('--name', type=str, help='Название группы')
    parser_group_comm.add_argument('--adminIds', type=str, help='Руководители')
    parser_group_comm.add_argument('--description', type=str, help='Описание группы')

    parser_group_comm = subparser_group.add_parser('add-member', help='Добавить участника в группу')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')
    parser_group_comm.add_argument('member', type=str, help='Участник (login для пользователя или имя для группы или подразделения)')
    

    parser_group_comm = subparser_group.add_parser('delete-member', help='Удалить участника из группы')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')
    parser_group_comm.add_argument('member', type=str, help='Участник (login для пользователя или имя для группы или подразделения)')

    parser_group_comm = subparser_group.add_parser('delete', help='Удалить группу')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')

    parser_group_comm = subparser_group.add_parser('show', help='Показать информацию о группе')
    parser_group_comm.add_argument('label', type=str, help='Имя группы')

    parser_group_comm = subparser_group.add_parser('show-all', help='Показать список групп ')
    parser_group_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_group_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_group_comm.add_argument('--csv', type=str, help='Выгрузить в CSV файл')

    parser_department = subparsers.add_parser('department', help='Действия над подразделением')
    subparser_department = parser_department.add_subparsers(help='Действия над подразделением', dest='sub_com_department')

    parser_department_comm = subparser_department.add_parser('create', help='Создать подразделение')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('name', type=str, help='Название подразделения')
    parser_department_comm.add_argument('--parentlabel', type=str, help='Имя родительского подразделения')
    parser_department_comm.add_argument('--headlabel', type=str, help='Login руководителя подразделения')
    parser_department_comm.add_argument('--description', type=str, help='Описание подразделения')

    parser_department_comm = subparser_department.add_parser('update', help='Изменить подразделение')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('--newlabel', type=str, help='Новое имя подразделения')
    parser_department_comm.add_argument('--parentlabel', type=str, help='Имя родительского подразделения')
    parser_department_comm.add_argument('--name', type=str, help='Название подразделения')
    parser_department_comm.add_argument('--headnickname', type=str, help='Login руководителя подразделения')
    parser_department_comm.add_argument('--description', type=str, help='Описание подразделения')

    parser_department_comm = subparser_department.add_parser('add-alias', help='Добавить алиас подразделению')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('alias', type=str, help='alias')

    parser_department_comm = subparser_department.add_parser('delete-alias', help='Удалить алиас у подразделения')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm.add_argument('alias', type=str, help='alias')

    parser_department_comm = subparser_department.add_parser('delete', help='Удалить подразделение')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm = subparser_department.add_parser('show', help='Показать информацию о подразделении')
    parser_department_comm.add_argument('label', type=str, help='Имя подразделения')
    parser_department_comm = subparser_department.add_parser('show-all', help='Показать список подразделений')
    parser_department_comm.add_argument('--page', type=int, help='Номер страницы')
    parser_department_comm.add_argument('--perPage', type=int, help='Количество записей на странице')
    parser_department_comm.add_argument('--parentId', type=int, help='Идентификатор родителя')
    parser_department_comm.add_argument('--orderBy', choices=['id','name'], help='Сортировать по')
    parser_department_comm.add_argument('--csv', type=str, help='Выгрузить в CSV файл')

    parser_config = subparsers.add_parser('make-config', help='Создание конфигурационного файла')
    
    return parser

def start():
    config = yao.load_token(path[0])
    if config is False:
        make_config()
        exit(0)

    if yao.check_expire_token(config, datetime.timedelta(days=30)):
        yao.save_token(path[0],yao.refresh_token(config))

    parser = gen_parser()
    args = parser.parse_args()


    if args.sub_com == None:
        parser.print_help()

    if args.sub_com == 'whois':
        whois(args)

    if args.sub_com == 'make-config':
        make_config()

    if args.sub_com == 'group':
        if args.sub_com_group == 'show':
            show_group(args)
        if args.sub_com_group == 'show-all':
            show_groups(args)
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

    if args.sub_com == 'department':
        if args.sub_com_department == 'show':
            show_department(args)
        if args.sub_com_department == 'show-all':
            show_departments(args)
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

    if args.sub_com == 'user':
        if args.sub_com_user == 'show':
            show_user(args)
        if args.sub_com_user == 'show-all':
            show_users(args)
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

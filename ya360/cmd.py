"""
Модуль командной строки
"""

import argparse
import datetime
from yandex_oauth import yao
from . import __version__
from . import __path__ as path
from .departments import create_department, update_department, add_alias_department, delete_alias_department, delete_department, show_department, show_departments
from .users import show_users, show_user, update_user, create_user, add_alias_user, delete_alias_user, delete_user, upload_avatar_user
from .groups import create_group, delete_group, update_group, add_member_group, delete_member_group, show_group, show_groups
from .mail import (edit_access_mailbox, delete_access_mailbox, show_status_access_mailbox,
    show_access_mailbox_user, show_users_access_mailbox,show_main_address,
    show_signs, edit_main_address, save_sign_to_file,
    edit_sign_param, add_sign, delete_sign,
    edit_sign_position, show_rules_user, add_rule_autoreplies,
    add_rule_forwards, delete_rule)
from .whois import whois
from .logs import show_mail_log, show_disk_log
from .configure import make_config
from .antispam import show_whitelist, add_in_whitelist, remove_from_whitelist, delete_whitelist
from .routing import add_in_routing, show_routing, remove_from_routing


def gen_parser():
    """Функция запуска приложения приема аргументов командной строки
    """
    parser = argparse.ArgumentParser(prog='ya360', description='Утилита командной строки для Yandex 360', epilog='Подробная документация находится по адресу https://ya360.readthedocs.io/')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s '+__version__)

    subparsers = parser.add_subparsers(dest='sub_com')


    parser_whois = subparsers.add_parser('whois', help='Кто это?')
    parser_whois.add_argument('name', type=str, help='nickname, alias или label разыскиваемой сущности')


    parser_user = subparsers.add_parser('user', help='Действия над пользователем')
    subparser_user = parser_user.add_subparsers(dest='sub_com_user')

    parser_user_comm = subparser_user.add_parser('create',help='Создать пользователя')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('name', nargs='*', help='Фамилия Имя Отчество')
    parser_user_comm.add_argument('password', type=str, help='Пароль')
    parser_user_comm.add_argument('--displayName', type=str, help='displayName')
    parser_user_comm.add_argument('--departmentId', type=int, default=1, help='ID подразделения')
    parser_user_comm.add_argument('--about', type=str, help='Описание пользователя')
    parser_user_comm.add_argument('--birthday', type=str, help='YYYY-MM-DD')
    parser_user_comm.add_argument('--phone', type=str, help='Телефонный номер')
    parser_user_comm.add_argument('--gender', type=str, help='Пол')
    parser_user_comm.add_argument('--isAdmin', choices=['true', 'false'], help='Признак администратора организации')
    parser_user_comm.add_argument('--language', type=str, help='Язык')
    parser_user_comm.add_argument('--position', type=str, help='Должность')
    parser_user_comm.add_argument('--timezone', type=str, help='Часовой пояс')

    parser_user_comm = subparser_user.add_parser('update', help='Изменить данные пользователя')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('--displayName', type=str, help='displayName')
    parser_user_comm.add_argument('--name', nargs='*', help='Фамилия Имя Отчество')
    parser_user_comm.add_argument('--about', type=str, help='Описание пользователя')
    parser_user_comm.add_argument('--birthday', type=str, help='YYYY-MM-DD')
    parser_user_comm.add_argument('--phone', type=str, help='Телефонный номер')
    parser_user_comm.add_argument('--departmentId', type=int, help='ID подразделения')
    parser_user_comm.add_argument('--gender', type=str, help='Пол')
    parser_user_comm.add_argument('--isAdmin', choices=['true', 'false'], help='Признак администратора организации')
    parser_user_comm.add_argument('--isEnabled', choices=['true', 'false'], help='Статус аккаунта')
    parser_user_comm.add_argument('--language', type=str, help='Язык')
    parser_user_comm.add_argument('--password', type=str, help='Пароль')
    parser_user_comm.add_argument('--passwordChangeRequired', choices=['true', 'false'], help='Обязательность изменения пароля при первом входе')
    parser_user_comm.add_argument('--position', type=str, help='Должность')
    parser_user_comm.add_argument('--timezone', type=str, help='Часовой пояс')

    parser_user_comm = subparser_user.add_parser('delete', help='Удалить пользователя '
                                                '(ВНИМАНИЕ! НЕОБРАТИМАЯ ОПЕРАЦИЯ! БУДУТ УДАЛЕНЫ ВСЕ ПОЧТОВЫЕ СООБЩЕНИЯ И ФАЙЛЫ НА ДИСКЕ!)')
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

    parser_user_comm = subparser_user.add_parser('avatar', help='Загрузить портрет пользователя')
    parser_user_comm.add_argument('nickname', type=str, help='Login пользователя')
    parser_user_comm.add_argument('filename', type=str, help='Имя файла')

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


    parser_mailbox = subparsers.add_parser('mailbox', help='Операции с почтовыми ящиками и отправителями')
    subparser_mailbox = parser_mailbox.add_subparsers(dest='sub_com_mailbox')

    parser_mailbox_comm = subparser_mailbox.add_parser('delegated',help='Делегирование доступа к почтовому ящику')
    parser_mailbox_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_mailbox_comm.add_argument('to_nickname', type=str, help='Login пользователя кому делегируем')
    parser_mailbox_comm.add_argument('--imap_full_access', action='store_true', help='право на чтение почты и управление настройками ящика')
    parser_mailbox_comm.add_argument('--send_on_behalf', action='store_true', help='право на отправление писем от своего имени')
    parser_mailbox_comm.add_argument('--send_as', action='store_true', help='право на отправление писем от имени владельца ящика')

    parser_mailbox_comm = subparser_mailbox.add_parser('delete',help='Удалить доступ к почтовому ящику')
    parser_mailbox_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_mailbox_comm.add_argument('to_nickname', type=str, help='Login пользователя у кого удаляются права')

    parser_mailbox_comm = subparser_mailbox.add_parser('status',help='Статус выполнения задачи')
    parser_mailbox_comm.add_argument('taskid', type=str, help='Номер задания')

    parser_mailbox_comm = subparser_mailbox.add_parser('list-mailboxes',help='Список почтовых ящиков, к которым у сотрудника есть права доступа')
    parser_mailbox_comm.add_argument('nickname', type=str, help='Login пользователя')

    parser_mailbox_comm = subparser_mailbox.add_parser('list-users',help='Список сотрудников, у которых есть права доступа к почтовому ящику')
    parser_mailbox_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')

    parser_sender_mailbox =  subparser_mailbox.add_parser('sender', help='Управление отправителем')
    subparser_sender_mailbox = parser_sender_mailbox.add_subparsers(dest='sub_com_sender_mailbox')

    parser_main_address = subparser_sender_mailbox.add_parser('main-address', help='Управление основным адресом')
    subparser_main_address = parser_main_address.add_subparsers(dest='sub_com_main_address')
    parser_main_address_comm =  subparser_main_address.add_parser('show', help='Отобразить основной адрес')
    parser_main_address_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_main_address_comm =  subparser_main_address.add_parser('edit', help='Изменить основной адрес')
    parser_main_address_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_main_address_comm.add_argument('defaultFrom', type=str, help='Основлной адрес')

    parser_sender_comm =  subparser_sender_mailbox.add_parser('sign-position', help='Расположение подписей')
    parser_sender_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_sender_comm.add_argument('position', type=str, choices=['bottom','under'], help='Расположение (bottom: под всем письмом, under: после ответа)')

    parser_signs = subparser_sender_mailbox.add_parser('signs', help='Управление подписями')
    subparser_signs = parser_signs.add_subparsers(dest='sub_com_signs')
    parser_signs_comm =  subparser_signs.add_parser('show', help='Отобразить подписи')
    parser_signs_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_signs_comm =  subparser_signs.add_parser('save', help='Сохранить подпись в файл')
    parser_signs_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_signs_comm.add_argument('num', type=int, help='Номер подписи')
    parser_signs_comm.add_argument('filename', type=str, help='Имя файла')
    parser_signs_comm = subparser_signs.add_parser('add', help='Добавить новую подпись')
    parser_signs_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_signs_comm.add_argument('isDefault', type=str, choices=['True','False'], help='Признак основной подписи')
    parser_signs_comm.add_argument('emails', type=str, help='Список адресов для ассоциирования')
    parser_signs_comm.add_argument('lang', type=str, help='Язык')
    parser_signs_comm.add_argument('filename', type=str, help='Имя файла с текстом подписи')
    parser_signs_comm = subparser_signs.add_parser('edit', help='Редактировать подпись')
    parser_signs_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_signs_comm.add_argument('num', type=int, help='Номер подписи')
    parser_signs_comm.add_argument('--isDefault', type=str, choices=['True','False'], help='Признак основной подписи')
    parser_signs_comm.add_argument('--emails', type=str, help='Список адресов для ассоциирования')
    parser_signs_comm.add_argument('--lang', type=str, help='Язык')
    parser_signs_comm.add_argument('--filename', type=str, help='Имя файла с текстом подписи')
    parser_signs_comm = subparser_signs.add_parser('delete', help='Удалить подпись')
    parser_signs_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_signs_comm.add_argument('num', type=int, help='Номер подписи')

    parser_rules = subparser_sender_mailbox.add_parser('rules', help='Управление правилами автоответа и переадресации')
    subparser_rules = parser_rules.add_subparsers(dest='sub_com_rules')
    parser_rules_comm =  subparser_rules.add_parser('show', help='Список правил')
    parser_rules_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_rules_comm =  subparser_rules.add_parser('add-autoreplies', help='Добавить правило автоответа')
    parser_rules_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_rules_comm.add_argument('ruleName', type=str, help='Наименование правила')
    parser_rules_comm.add_argument('text', type=str, help='Текст автоответа')
    parser_rules_comm =  subparser_rules.add_parser('add-forwards', help='Добавить правило пересылки')
    parser_rules_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_rules_comm.add_argument('ruleName', type=str, help='Наименование правила')
    parser_rules_comm.add_argument('address', type=str, help='Адрес получателя')
    parser_rules_comm.add_argument('copy', type=str, choices=['True','False'], help='Сохранять копию письма')
    parser_rules_comm =  subparser_rules.add_parser('delete', help='Удалить правило')
    parser_rules_comm.add_argument('nickname', type=str, help='Login пользователя почтового ящика')
    parser_rules_comm.add_argument('ruleId', type=int, help='Номер правила')



    parser_logs = subparsers.add_parser('logs', help='Аудит-лог событий в организации')
    subparser_logs = parser_logs.add_subparsers(dest='sub_com_logs')

    parser_logs_comm = subparser_logs.add_parser('mail',help='Аудит-лог почты')
    parser_logs_comm.add_argument('--beforeDate', type=str, help='Верхняя граница периода выборки в формате ISO 8601')
    parser_logs_comm.add_argument('--afterDate', type=str, help='Нижняя граница периода выборки в формате ISO 8601')
    parser_logs_comm.add_argument('--includeUsers', type=str, help='Список пользователей, действия которых должны быть включены в список событий')
    parser_logs_comm.add_argument('--excludeUsers', type=str, help='Список пользователей, действия которых должны быть исключены из списка событий')
    parser_logs_comm.add_argument('--types', type=str, help='Типы событий которые должны быть включены в список. По умолчанию включаются все события')
    parser_logs_comm.add_argument('--csv', type=str, help='Выгрузить в CSV файл')

    parser_logs_comm = subparser_logs.add_parser('disk',help='Аудит-лог диска')
    parser_logs_comm.add_argument('--beforeDate', type=str, help='Верхняя граница периода выборки в формате ISO 8601')
    parser_logs_comm.add_argument('--afterDate', type=str, help='Нижняя граница периода выборки в формате ISO 8601')
    parser_logs_comm.add_argument('--includeUsers', type=str, help='Список пользователей, действия которых должны быть включены в список событий')
    parser_logs_comm.add_argument('--excludeUsers', type=str, help='Список пользователей, действия которых должны быть исключены из списка событий')
    parser_logs_comm.add_argument('--types', type=str, help='Типы событий которые должны быть включены в список. По умолчанию включаются все события')
    parser_logs_comm.add_argument('--csv', type=str, help='Выгрузить в CSV файл')

    parser_antispam = subparsers.add_parser('antispam', help='Антиспам')
    subparser_antispam = parser_antispam.add_subparsers(dest='sub_com_antispam')
    parser_antispam_comm = subparser_antispam.add_parser('show', help='Показать содержимое белого списка')
    parser_antispam_comm = subparser_antispam.add_parser('add', help='Добавить в белый список')
    parser_antispam_comm.add_argument('ipcidr', type=str, help='Адрес или CIDR')
    parser_antispam_comm = subparser_antispam.add_parser('remove', help='Удалить из белого списка')
    parser_antispam_comm.add_argument('ipcidr', type=str, help='Адрес или CIDR')
    parser_antispam_comm = subparser_antispam.add_parser('delete', help='Очистить белый список')

    parser_routing = subparsers.add_parser('routing', help='Правила маршрутизации')
    subparser_routing = parser_routing.add_subparsers(dest='sub_com_routing')
    parser_routing_comm = subparser_routing.add_parser('show', help='Показать содержимое таблицы правил')
    parser_routing_comm = subparser_routing.add_parser('add', help='Добавить правило')
    parser_routing_comm.add_argument('rule', type=str, help='Правило')
    parser_routing_comm.add_argument('-P', '--position', type=int, help='Позиция')
    parser_routing_comm = subparser_routing.add_parser('remove', help='Удалить правило')
    parser_routing_comm.add_argument('position', type=int, help='Позиция')


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
        if args.sub_com_user == 'avatar':
            upload_avatar_user(args)

    if args.sub_com == 'mailbox':
        if args.sub_com_mailbox == 'delegated':
            edit_access_mailbox(args)
        if args.sub_com_mailbox == 'delete':
            delete_access_mailbox(args)
        if args.sub_com_mailbox == 'status':
            show_status_access_mailbox(args)
        if args.sub_com_mailbox == 'list-mailboxes':
            show_access_mailbox_user(args)
        if args.sub_com_mailbox == 'list-users':
            show_users_access_mailbox(args)
        if args.sub_com_mailbox == 'sender':
            if args.sub_com_sender_mailbox == 'main-address':
                if args.sub_com_main_address == 'show':
                    show_main_address(args)
                if args.sub_com_main_address == 'edit':
                    edit_main_address(args)
            if args.sub_com_sender_mailbox == 'signs':
                if args.sub_com_signs == 'show':
                    show_signs(args)
                if args.sub_com_signs == 'save':
                    save_sign_to_file(args)
                if args.sub_com_signs == 'edit':
                    edit_sign_param(args)
                if args.sub_com_signs == 'add':
                    add_sign(args)
                if args.sub_com_signs == 'delete':
                    delete_sign(args)
            if args.sub_com_sender_mailbox == 'sign-position':
                edit_sign_position(args)
            if args.sub_com_sender_mailbox == 'rules':
                if args.sub_com_rules == 'show':
                    show_rules_user(args)
                if args.sub_com_rules == 'add-autoreplies':
                    add_rule_autoreplies(args)
                if args.sub_com_rules == 'add-forwards':
                    add_rule_forwards(args)
                if args.sub_com_rules == 'delete':
                    delete_rule(args)
                

    if args.sub_com == 'logs':
        if args.sub_com_logs == 'mail':
            show_mail_log(args)
        if args.sub_com_logs == 'disk':
            show_disk_log(args)

    if args.sub_com == 'antispam':
        if args.sub_com_antispam == 'show':
            show_whitelist()
        if args.sub_com_antispam == 'add':
            add_in_whitelist(args)
        if args.sub_com_antispam == 'remove':
            remove_from_whitelist(args)
        if args.sub_com_antispam == 'delete':
            delete_whitelist()

    if args.sub_com == 'routing':
        if args.sub_com_routing == 'show':
            show_routing()
        if args.sub_com_routing == 'add':
            add_in_routing(args)
        if args.sub_com_routing == 'remove':
            remove_from_routing(args)

Справочник команд
-----------------

.. argparse::
   :module: ya360.cmd
   :func: gen_parser
   :prog: ya360
   :noepilog:

   group : @skip
      delete : @before
         .. danger::
            Данную операцию невозможно отменить!
   
   department : @skip
      delete : @before
         .. danger::
            Данную операцию невозможно отменить!

   antispam : @skip
      delete : @before
         .. danger::
            Данную операцию невозможно отменить!

   user : @skip
      delete : @replace
         .. danger::
            Данная операция необратима! Удаление пользователя приведет к моментальному
            удалению всех данных в почте и на диске!

   routing : @replace
      .. warning::
         Экспериментальный набор команд для правил маршрутизации почты. Доступен ограниченному набору тестировщиков.

import logging
import logging.handlers
import os

"""
Для проекта «Мессенджер» реализовать логирование с использованием модуля logging:
В директории проекта создать каталог log, в котором для клиентской и серверной сторон в отдельных модулях формата 
client_log_config.py и server_log_config.py создать логгеры;
В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
Создание именованного логгера;
Сообщения лога должны иметь следующий формат: "<дата-время> <уровень_важности> <имя_модуля> <сообщение>";
Журналирование должно производиться в лог-файл;
На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.    
Реализовать применение созданных логгеров для решения двух задач:
Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование 
и обеспечить вывод служебных сообщений в лог-файл;
Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

"""


def init_logger(name_app,
                format_logger="%(asctime)s :: %(levelname)s :: %(module)s :: %(message)s",
                log_dir='log/logs',
                log_file_name='server.log',
                backup_count=10,
                interval=1,
                when='D',
                encoding='utf-8'):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log = logging.getLogger(name_app)
    log.setLevel(logging.DEBUG)
    frh = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(log_dir, log_file_name),
        backupCount=backup_count,  # хотя не просили, ну да ладно, надеюсь ни чего страшного... :)
        interval=interval,
        when=when,
        encoding=encoding
    )
    frh.setLevel(logging.DEBUG)
    frh.setFormatter(logging.Formatter(format_logger))
    log.addHandler(frh)
    log.debug('Логгер создан')

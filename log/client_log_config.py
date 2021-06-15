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
                log_file_name='client.log',
                encoding='utf-8'):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log = logging.getLogger(name_app)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(
        filename=os.path.join(log_dir, log_file_name),
        encoding=encoding
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(format_logger))
    log.addHandler(fh)
    log.debug('Логгер создан')

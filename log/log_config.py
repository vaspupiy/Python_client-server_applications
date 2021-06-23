import logging
import logging.handlers
import os

FORMAT_LOGGER = "%(asctime)s :: %(levelname)s :: %(module)s :: %(message)s"
LOG_PATH_SERVER = 'log/logs/server.log'
LOG_PATH_CLIENT = 'log/logs/client.log'
BACKUP_COUNT = 10
INTERVAL = 1
WHEN = 'D'
ENCODING = 'utf-8'

log_serv = logging.getLogger('tcp_server_log')
log_serv.setLevel(logging.DEBUG)
frh = logging.handlers.TimedRotatingFileHandler(
    LOG_PATH_SERVER,
    backupCount=BACKUP_COUNT,
    interval=INTERVAL,
    when=WHEN,
    encoding=ENCODING
)
frh.setLevel(logging.DEBUG)
frh.setFormatter(logging.Formatter(FORMAT_LOGGER))
log_serv.addHandler(frh)

log_client = logging.getLogger('tcp_client_log')
log_client.setLevel(logging.DEBUG)
fh = logging.FileHandler(
    LOG_PATH_CLIENT,
    encoding=ENCODING
)
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(FORMAT_LOGGER))
log_client.addHandler(fh)

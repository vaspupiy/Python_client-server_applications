import logging
from functools import wraps
from socket import AF_INET, socket, SOCK_STREAM
from datetime import datetime
from argparse import ArgumentParser
import pickle

from log.client_log_config import init_logger


def log(func):
    if not logging.getLogger('tcp_client_log').handlers:
        init_logger('tcp_client_log')
        _logger = logging.getLogger('tcp_client_log')
    else:
        _logger = logging.getLogger('tcp_client_log')

    @wraps(func)
    def call(*args, **kwargs):
        _logger.debug(f'!произошел вызов ф-ии: {func.__name__}::'
                      f' позиционные аркументы: {args}:: '
                      f'именованные аргументы: {kwargs}')
        r = func(*args, **kwargs)
        _logger.debug(f'!функция: {func.__name__}:: вернула {r}')
        return r

    return call


@log
def create_presence(_time: datetime, name="Гость", status="Тут!") -> dict:
    """формирует presence-сообщение"""
    _msg = {
        "action": "presence",
        "time": str(_time),
        "type": "status",
        "user": {
            "account_name": name,
            "status": status
        }
    }
    return _msg


@log
def dumps_message(_msg: dict) -> bytes:
    return pickle.dumps(_msg)


@log
def send_message(_connect: socket, _msg: bytes):
    """отправляет сообщение серверу"""
    _connect.send(_msg)


@log
def receive_message(_connect: socket, data_volume) -> bytes:
    """принимает сообщение от сервера"""
    return _connect.recv(data_volume)


@log
def parse_message(_data: bytes) -> dict:
    """разбирает сообщение сервера"""
    pars_data = pickle.loads(_data)
    return pars_data


@log
def get_args(_host: str, _port: int):
    parser = ArgumentParser()
    parser.add_argument("--addr", help="IP-адрес для прослушивания", type=str, default=_host)
    parser.add_argument("--port", help="TCP-порт для работы", type=int, default=_port)
    _args = parser.parse_args()

    if 1023 > _args.port or _args.port > 65535:
        raise ValueError(f"Неверное значение порта ({_args.port}) ожидается: (1023 < --port < 65535)")
    return _args


@log
def set_socket_connection(_host: str, _port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((_host, _port))
    return s


@log
def main(_host, _port, _time, _logger, _len_message=4096, testing=False):
    _logger.debug(f'параметры ф-ии main: "{_host}"::"{_port}"::"{_time}"::"{_len_message}"::"{testing}"')
    args = get_args(_host, _port)
    _logger.debug(f'получены значения хоста: {args.addr} и порта: {args.port}')
    socket_connection = set_socket_connection(args.addr, args.port)
    _logger.debug(f' установленно соединение: {socket_connection}')
    msg = create_presence(_time)
    _logger.debug(f'создано сообщение: {msg}')
    msg_byte = dumps_message(msg)
    _logger.debug(f'сообщение закодировано для отправки: {msg_byte}')
    send_message(socket_connection, msg_byte)
    _logger.debug(f'сообщение отпралено')
    if testing:
        return
    data_bytes = receive_message(socket_connection, _len_message)
    _logger.debug(f'получено сообщение от сервера: {data_bytes}')
    message_from_server = parse_message(data_bytes)
    _logger.debug(f'сообщение декодировано: {message_from_server}')
    _logger.info(f'Сообщения от сервера: "{message_from_server["alert"]}"')
    socket_connection.close()
    _logger.debug(f'соединение закрыто')


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 7777
    TIME = datetime.now()
    LEN_RECEIVE_MASSAGE = 1024

    if not logging.getLogger('tcp_client_log').handlers:
        init_logger('tcp_client_log')
        logger = logging.getLogger('tcp_client_log')
    else:
        logger = logging.getLogger('tcp_client_log')

    logger.debug('поехали')

    try:
        main(HOST, PORT, TIME, logger, LEN_RECEIVE_MASSAGE, )
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали')

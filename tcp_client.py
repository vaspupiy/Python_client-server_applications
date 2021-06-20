import logging
from functools import wraps
from socket import AF_INET, socket, SOCK_STREAM
from datetime import datetime
from argparse import ArgumentParser
import pickle

from log.log_config import log_client as logger


def log(func):
    # if not logging.getLogger('tcp_client_log').handlers:
    #     init_logger('tcp_client_log')
    #     _logger = logging.getLogger('tcp_client_log')
    # else:
    #     _logger = logging.getLogger('tcp_client_log')

    @wraps(func)
    def call(*args, **kwargs):
        logger.debug(f'!произошел вызов ф-ии: {func.__name__}::'
                     f' позиционные аркументы: {args}:: '
                     f'именованные аргументы: {kwargs}')
        r = func(*args, **kwargs)
        logger.debug(f'!функция: {func.__name__}:: вернула {r}')
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
def create_msg(_time: datetime, _input_msg: str, name="Гость") -> dict:
    """формирует presence-сообщение"""
    _msg = {
        "action": "msg",
        "time": _time,
        "to": "#all",
        "from": name,
        "message": _input_msg
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
def encode_message(_data: bytes) -> dict:
    """преобразует в словарь"""
    pars_data = pickle.loads(_data)
    return pars_data


@log
def parse_message(_data: dict) -> str:
    """разбирает сообщение сервера, пока только Пользователь-Чат (согласно заданию)"""
    if _data["action"]:
        if _data["action"] == 'msg':  # а есть ли случаи, когда входящий "action" не "msg"?... На всяки проверю...
            return _data["message"]


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
def read_or_write(_attempt=3) -> str:
    for _ in range(_attempt):
        _client_type = input('Укажите, кто Вы - читатель(r) или писатель(w) :')
        if _client_type.lower() == 'r' or _client_type.lower() == 'w':
            return _client_type
        print("Не верно указан тип пользователя, необходимо ввести либо (r) либо (w) ")
    print('Вы читатель!')
    return 'r'


@log
def main(_host, _port, _time: datetime, _client_type: str, _len_message=4096, _name="Гость"):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((_host, _port))

        if _client_type == 'w':
            while True:
                msg = input('Ваше сообщение: ')
                if msg == 'exit':
                    break
                send_msg = create_msg(_time, msg, _name)
                msg_byte = dumps_message(send_msg)
                send_message(sock, msg_byte)

        else:
            while True:
                data_bytes = receive_message(sock, _len_message)
                encode_msg = encode_message(data_bytes)
                message_from_server = parse_message(encode_msg)
                print('Ответ: ', message_from_server)


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 7777
    TIME = datetime.now()
    LEN_RECEIVE_MASSAGE = 1024

    client_type = read_or_write()

    # if not logging.getLogger('tcp_client_log').handlers:
    #     init_logger('tcp_client_log')
    #     logger = logging.getLogger('tcp_client_log')
    # else:
    #     logger = logging.getLogger('tcp_client_log')

    logger.debug('поехали')

    try:
        main(HOST, PORT, TIME, client_type, LEN_RECEIVE_MASSAGE, )
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали')

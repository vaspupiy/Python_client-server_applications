import logging
import time
from functools import wraps
from socket import AF_INET, socket, SOCK_STREAM
from datetime import datetime
from argparse import ArgumentParser
import pickle
from threading import Thread

from log.log_config import log_client as logger


def log(func):
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
def receive_message(_connect: socket, data_volume: int) -> bytes:
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
    if "action" in _data:
        if _data["action"] == 'msg':
            return _data["message"]
        elif _data["action"] == 'probe':
            return 'probe'


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


def join_chat():
    pass


def leave_chat():
    pass


def create_and_send_msg():
    pass


@log
def write_messages(_time, _sock, _name):
    while True:
        msg = input('Что будем делать?\n Вступить в чат (j) \n Выйти из чата (l) \nОтправить сообщение(m) '
                    '\nВыйти и пойти куда глаза глядят (q)')
        if msg == 'q':
            return
        elif msg == 'j':
            join_chat()
        elif msg == 'l':
            leave_chat()
        elif msg == 'm':
            create_and_send_msg()
        # send_msg = create_msg(_time, msg, _name)
        # msg_byte = dumps_message(send_msg)
        # send_message(_sock, msg_byte)


@log
def send_receive_presence(_sock, _time, _len_message) -> dict:
    msg = create_presence(_time)
    byte_msg = dumps_message(msg)
    send_message(_sock, byte_msg)
    data_bytes = receive_message(_sock, _len_message)
    return encode_message(data_bytes)


@log
def read_messages(_sock, _time, _len_message):
    while True:
        data_bytes = receive_message(_sock, _len_message)
        encode_msg = encode_message(data_bytes)
        message_from_server = parse_message(encode_msg)
        if message_from_server == 'probe':
            send_receive_presence(_sock, _time, _len_message)
        print('Ответ: ', message_from_server)


def create_thread(_sock, _time, _len_message, _name):
    # прием сообщений
    r_thread = Thread(target=read_messages, daemon=True, args=(_sock, _time, _len_message))
    r_thread.start()

    # Отправка сообщений
    w_thread = Thread(target=write_messages, args=(_time, _sock, _name))
    w_thread.start()


@log
def main(_host, _port, _time: datetime, _len_message=4096, _name="Гость"):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((_host, _port))
    encode_msg = send_receive_presence(sock, _time, _len_message)
    print(encode_msg)
    if encode_msg['response'] == 200:
        print(1)
        print(encode_msg["alert"])
        create_thread(sock, _time, _len_message, _name)
    else:
        print(encode_msg['response'], encode_msg['error'])


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 7777
    TIME = datetime.now()
    LEN_RECEIVE_MASSAGE = 1024

    logger.debug('поехали')

    try:
        main(HOST, PORT, TIME, LEN_RECEIVE_MASSAGE, )
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали')

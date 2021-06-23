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
def create_presence(_time: datetime, _name, status="Тут!") -> dict:
    """формирует presence-сообщение"""
    _msg = {
        "action": "presence",
        "time": str(_time),
        "type": "status",
        "user": {
            "account_name": _name,
            "status": status
        }
    }
    return _msg


@log
def create_msg(_time: datetime, _to: str, _input_msg: str, _name) -> dict:
    """формирует presence-сообщение"""
    _msg = {
        "action": "msg",
        "time": str(_time),
        "to": _to,
        "from": _name,
        "message": _input_msg
    }
    return _msg


def join_leave_chat(_time: datetime, _action: str, _room) -> dict:
    _msg = {
        "action": _action,
        "time": str(_time),
        "room": _room,
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
    elif "response" in _data:
        return _data['alert']


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
    user_input = input('К какому чату желаете присоединиться?: \n"Зрящие во все корни" - (z)'
                       '\n"Хладнокровные чревоугодники" (a) \nДа ну на фиг (все остальное)\n')
    if user_input == 'z':
        room = '#Зрящие во все корни'
    elif user_input == 'a':
        room = '#Хладнокровные чревоугодники'
    else:
        return
    return room

    # msg = join_leave_chat(_time, 'join', room)
    # byte_msg = dumps_message(msg)
    # send_message(_connect, byte_msg)


def leave_chat():
    user_input = input('От какого чата желаете отключиться?: \n"Зрящие во все корни" - (z)'
                       '\n"Хладнокровные чревоугодники" (a) \nДа ну на фиг (все остальное)\n')
    if user_input == 'z':
        room = '#Зрящие во все корни'
    elif user_input == 'a':
        room = '#Хладнокровные чревоугодники'
    else:
        return
    return room


def create_param_msg():
    user_input = input('Куда отправить собщение?:'
                       '\n в чат "Зрящие во все корни" - (z)'
                       '\nв чат "Хладнокровные чревоугодники" (a)'
                       '\nПользователю (u)'
                       '\nДа ну на фиг (все остальное)\n')
    if user_input == 'z':
        _to = '#Зрящие во все корни'
    elif user_input == 'a':
        _to = '#Хладнокровные чревоугодники'
    elif user_input == 'u':
        _to = input('Введите имя пользователя, кому отправим\n').capitalize()
    else:
        return
    return _to


@log
def write_messages(_time, _sock, _name):
    while True:
        _msg = None
        user_input = input('Что будем делать?\nВступить в чат (j) \nВыйти из чата (l) \nОтправить сообщение(m)'
                           '\nВыйти и пойти куда глаза глядят (q)\n')
        if user_input == 'q':
            return
        elif user_input == 'j':
            _room = join_chat()
            if _room:
                _msg = join_leave_chat(_time, 'join', _room)
        elif user_input == 'l':
            _room = leave_chat()
            if _room:
                _msg = join_leave_chat(_time, 'leave', _room)
        elif user_input == 'm':
            _to = create_param_msg()
            user_msg = input('Введите сообщение\n')
            if user_msg:
                _msg = create_msg(_time, _to, user_msg, _name)
        if _msg:
            msg_byte = dumps_message(_msg)
            send_message(_sock, msg_byte)


@log
def send_receive_presence(_sock, _time, _len_message, _name) -> dict:
    msg = create_presence(_time, _name)
    byte_msg = dumps_message(msg)
    send_message(_sock, byte_msg)
    data_bytes = receive_message(_sock, _len_message)
    return encode_message(data_bytes)


@log
def read_messages(_sock, _time, _len_message, _name):
    while True:
        data_bytes = receive_message(_sock, _len_message)
        encode_msg = encode_message(data_bytes)
        message_from_server = parse_message(encode_msg)
        if message_from_server == 'probe':
            send_receive_presence(_sock, _time, _len_message, _name)
        print('\nПолучено сообщение: ', message_from_server, '\n')


def create_thread(_sock, _time, _len_message, _name):
    # прием сообщений
    r_thread = Thread(target=read_messages, daemon=True, args=(_sock, _time, _len_message, _name))
    r_thread.start()

    # Отправка сообщений
    w_thread = Thread(target=write_messages, args=(_time, _sock, _name))
    w_thread.start()


@log
def main(_host, _port, _time: datetime, _len_message=4096, _name="Гость"):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((_host, _port))
    encode_msg = send_receive_presence(sock, _time, _len_message, _name)
    if encode_msg['response'] == 200:
        create_thread(sock, _time, _len_message, _name)
    else:
        print(encode_msg['response'], encode_msg['error'])


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 7777
    TIME = datetime.now()
    LEN_RECEIVE_MASSAGE = 1024
    name = input('введите свое имя: \n').capitalize()
    print(f'Привет {name}')

    logger.debug('поехали')

    try:
        main(HOST, PORT, TIME, LEN_RECEIVE_MASSAGE, name)
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали')

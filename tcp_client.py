from socket import AF_INET, socket, SOCK_STREAM
from datetime import datetime
from argparse import ArgumentParser
import pickle


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


def dumps_message(_msg: dict) -> bytes:
    return pickle.dumps(_msg)


def send_message(_connect: socket, _msg: bytes):
    """отправляет сообщение серверу"""
    _connect.send(_msg)


def receive_message(_connect: socket, data_volume) -> bytes:
    """принимает сообщение от сервера"""
    return _connect.recv(data_volume)


def parse_message(_data: bytes) -> dict:
    """разбирает сообщение сервера"""
    pars_data = pickle.loads(_data)
    return pars_data


def get_args(_host: str, _port: int):
    parser = ArgumentParser()
    parser.add_argument("--addr", help="IP-адрес для прослушивания", type=str, default=_host)
    parser.add_argument("--port", help="TCP-порт для работы", type=int, default=_port)
    _args = parser.parse_args()

    if 1023 > _args.port or _args.port > 65535:
        raise ValueError(f"Неверное значение порта ({_args.port}) ожидается: (1023 < --port < 65535)")
    return _args


def set_socket_connection(_host: str, _port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((_host, _port))
    return s


def main(_host, _port, _time, _len_message=4096):
    args = get_args(_host, _port)
    socket_connection = set_socket_connection(args.addr, args.port)
    msg = create_presence(_time)
    msg_byte = dumps_message(msg)
    send_message(socket_connection, msg_byte)
    data_bytes = receive_message(socket_connection, _len_message)
    message_from_server = parse_message(data_bytes)
    print('Сообщения от сервера ', message_from_server, type(message_from_server), ', длинной', len(data_bytes), 'байт')
    socket_connection.close()


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 7777
    TIME = datetime.now()
    LEN_RECEIVE_MASSAGE = 1024

    try:
        main(HOST, PORT, TIME, LEN_RECEIVE_MASSAGE)
    except Exception as error:
        print(error)
        with open('err_cl.txt', 'a+') as err_file:
            err_file.write(f'{TIME}; {error}, тип ошибки {type(error)} \n')

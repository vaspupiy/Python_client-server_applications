from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from datetime import datetime
from argparse import ArgumentParser
import pickle
import logging
from log.server_log_config import init_logger


def accepts_response(_data: dict, _logger) -> bytes:
    """формирует ответ клиенту"""
    _response = {
        "response": None,
        "alert": None
    }
    if _data["action"] == "presence":
        _response["response"] = 200
        _response["alert"] = "серверу пофиг!"
    _logger.debug(f'создан ответ от сервера: {_response}')
    return pickle.dumps(_response)


def parse_message(_data: bytes) -> dict:
    """разобирает сообщение сервера"""
    pars_data = pickle.loads(_data)
    return pars_data


def send_response_client(_client, _msg: bytes):
    """отправляет ответ клиенту"""
    _client.send(_msg)


def receive_message_from_client(_client, data_volume) -> bytes:
    """принимает сообщение от клиента"""
    return _client.recv(data_volume)


def get_args(_host: str, _port: int):
    parser = ArgumentParser()
    parser.add_argument("--addr", "-a", help="IP-адрес для прослушивания", type=str, default=_host)
    parser.add_argument("--port", "-p", help="TCP-порт для работы", type=int, default=_port)
    _args = parser.parse_args()
    if 1023 > _args.port or _args.port > 65535:
        raise ValueError(f"Неверное значение порта ({_args.port}) ожидается: (1023 < --port < 65535)")
    return _args


def set_socket_connection_serv(_host: str, _port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((_host, _port))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return s


def main(_host, _port, _logger, _len_message=4096, testing=False) -> None:
    _logger.debug(f'параметры ф-ии main: "{_host}"::"{_port}"::"{_len_message}"::"{testing}"')
    args = get_args(_host, _port)
    _logger.debug(f'получены значения хоста: {args.addr} и порта: {args.port}')
    socket_connection = set_socket_connection_serv(args.addr, args.port)
    _logger.debug(f' создано соединение: {socket_connection}')
    while True:
        _logger.debug('жду клиента')
        if testing:
            return
        client, addr = socket_connection.accept()
        _logger.debug(f'установлленно соединение с клиентом: {client}, адресс: {addr}')
        data_bytes = receive_message_from_client(client, _len_message)
        _logger.debug(f'получено сообщение: {data_bytes}: от клиента: {client}, длинной: {addr} байт')
        data = parse_message(data_bytes)
        _logger.debug(f'сообщение декодировано: {data}')
        _logger.info(f'Сообщение: {data}, было отправлено клиентом: {addr}')
        msg = accepts_response(data, _logger)
        _logger.info(f'создано ответное сообщение: {msg}')
        send_response_client(client, msg)
        _logger.info(f'ответное сообщение: {msg} отправлено {client}')
        client.close()
        _logger.debug(f'закрыто соединение с клиентом: {client}, адресс: {addr}')


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 7777
    LEN_RECEIVE_MASSAGE = 1024
    TIME = datetime.now()
    init_logger('tcp_server_log')
    logger = logging.getLogger('tcp_server_log')

    logger.debug('поехали')

    try:
        main(HOST, PORT, logger, LEN_RECEIVE_MASSAGE)
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали :)')

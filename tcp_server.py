from functools import wraps
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from datetime import datetime
from argparse import ArgumentParser
import pickle
import logging
from log.log_config import log_serv as logger
import select


def log(func):
    # if not logging.getLogger('tcp_server_log').handlers:
    #     init_logger('tcp_server_log')
    #     _logger = logging.getLogger('tcp_server_log')
    # else:
    #     _logger = logging.getLogger('tcp_server_log')

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
def accepts_response(_data: dict) -> dict:
    """формирует ответ клиенту"""
    _response = {
        "response": None,
        "alert": None
    }
    if _data["action"] == "presence":
        _response["response"] = 200
        _response["alert"] = "серверу пофиг!"
    elif _data["action"] == "msg":
        return _data
    return _response


@log
def encode_response(_response: dict) -> bytes:
    return pickle.dumps(_response)


@log
def parse_message(_data: bytes) -> dict:
    """разобирает сообщение клиента"""
    pars_data = pickle.loads(_data)
    return pars_data


@log
def send_response_client(_client, _msg: bytes) -> None:
    """отправляет ответ клиенту"""
    _client.send(_msg)


@log
def receive_message_from_client(_client, data_volume) -> bytes:
    """принимает сообщение от клиента"""
    return _client.recv(data_volume)


@log
def get_args(_host: str, _port: int):
    parser = ArgumentParser()
    parser.add_argument("--addr", "-a", help="IP-адрес для прослушивания", type=str, default=_host)
    parser.add_argument("--port", "-p", help="TCP-порт для работы", type=int, default=_port)
    _args = parser.parse_args()
    if 1023 > _args.port or _args.port > 65535:
        raise ValueError(f"Неверное значение порта ({_args.port}) ожидается: (1023 < --port < 65535)")
    return _args


@log
def set_socket_connection_serv(_host: str, _port: int):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((_host, _port))
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    return s


# @log слишком много событий :)
def read_requests(r_clients: list, all_clients: list, data_volume: int) -> dict:
    """ Чтение запросов списка клиентов"""
    responses = {}  # Словарь ответов сервкера вида {socket: request}

    for sock in r_clients:
        try:
            b_data = receive_message_from_client(sock, data_volume)
            responses[sock] = parse_message(b_data)
        except BaseException as e:
            print(e)
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)
    return responses


@log
def write_responses(requests: dict, w_clients: list, all_clients: list) -> None:
    """Эхо-ответ сервера клиентам, от которых были запросы"""
    for sock in w_clients:
        if sock in requests:
            try:
                response = accepts_response(requests[sock])
                b_response = encode_response(response)
                if "action" in response:
                    for client in all_clients:
                        send_response_client(client, b_response)
                else:
                    send_response_client(sock, b_response)
            except BaseException as e:
                print(e)
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                sock.close()
                all_clients.remove(sock)


@log
def main(_host, _port, _len_message=4096, testing=False) -> None:
    args = get_args(_host, _port)
    socket_connection = set_socket_connection_serv(args.addr, args.port)
    clients = []

    while True:
        if testing:
            return
        try:
            client, addr = socket_connection.accept()
        except OSError as e:
            pass
        else:
            print(f'Получен запрос на соединение от {str(addr)}')
            clients.append(client)
        finally:
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except OSError:
                pass
            requests = read_requests(r, clients, _len_message)
            if requests:
                write_responses(requests, w, clients)


if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 7777
    LEN_RECEIVE_MASSAGE = 1024
    TIME = datetime.now()

    # if not logging.getLogger('tcp_server_log').handlers:
    #     init_logger('tcp_server_log')
    #     logger = logging.getLogger('tcp_server_log')
    # else:
    #     logger = logging.getLogger('tcp_server_log')

    logger.debug('поехали')

    try:
        main(HOST, PORT, LEN_RECEIVE_MASSAGE)
    except Exception as error:
        logger.exception(error)

    logger.debug('приехали :)')

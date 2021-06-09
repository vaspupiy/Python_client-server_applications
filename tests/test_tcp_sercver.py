import pickle
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM

import pytest

from tcp_server import accepts_response, parse_message, send_response_client, receive_message_from_client, \
    set_socket_connection_serv, get_args, main

TIME = datetime.now()


@pytest.mark.parametrize("data_dict, expected_result", [
    (
            {
                "action": "presence",
                "time": str(TIME),
                "type": "status",
                "user": {
                    "account_name": "Гость",
                    "status": "Тут!"
                }
            },
            pickle.dumps(
                {
                    "response": 200,
                    "alert": 'серверу пофиг!'
                }
            )
    ),
    (
            {
                "action": "no_presence",
                "time": str(TIME),
                "type": "status",
                "user": {
                    "account_name": "Гость",
                    "status": "Тут!"
                }
            },
            pickle.dumps(
                {
                    "response": None,
                    "alert": None
                }
            )
    )
])
def test_accepts_response(data_dict, expected_result, create_logger_server):
    logger = create_logger_server
    assert accepts_response(data_dict, logger) == expected_result


def test_parse_message(create_logger_server):
    data = {
        "action": "no_presence",
        "time": "07.06.2021",
        "type": "status",
        "user": {
            "account_name": "Гость",
            "status": "Тут!"
        }
    }
    bytes_data = pickle.dumps(data)
    assert parse_message(bytes_data) == data


def test_send_response_client():
    s_serv = socket(AF_INET, SOCK_STREAM)
    s_serv.bind(('0.0.0.0', 7777))
    s_serv.listen(1)

    s_cl = socket(AF_INET, SOCK_STREAM)
    s_cl.connect(('localhost', 7777))

    client, addr = s_serv.accept()

    send_response_client(client, 'abc'.encode())

    s_cl.settimeout(1.0)
    msg_b = s_cl.recv(1024)
    assert msg_b
    client.close()
    s_cl.close()
    s_serv.close()


def test_get_args_good(crutch_for_terminal_input_function):
    assert get_args('localhost', 7777, ).addr == 'localhost'
    assert get_args('localhost', 7777, ).port == 7777


def test_receive_message_from_client():
    s_serv = socket(AF_INET, SOCK_STREAM)
    s_serv.bind(('0.0.0.0', 7777))
    s_serv.listen(1)

    s_cl = socket(AF_INET, SOCK_STREAM)
    s_cl.connect(('localhost', 7777))

    client, addr = s_serv.accept()

    s_cl.send('abc'.encode())

    s_cl.settimeout(1.0)
    msg_b = receive_message_from_client(client, 1024)
    assert msg_b
    client.close()
    s_cl.close()
    s_serv.close()


def test_set_socket_connection_serv():
    assert set_socket_connection_serv('0.0.0.0', 7777).getsockname() == ('0.0.0.0', 7777)


def test_main(create_logger_server):
    logger = create_logger_server
    assert main('0.0.0.0', 7777, logger, 1024, testing=True) is None




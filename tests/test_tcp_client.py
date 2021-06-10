import pickle
from argparse import ArgumentParser
from datetime import datetime

import pytest

from tcp_client import create_presence, dumps_message, get_args, set_socket_connection, send_message, receive_message, \
    parse_message, main

from socket import socket, AF_INET, SOCK_STREAM

TIME = datetime.now()


def test_create_presence_good_all_default():
    assert create_presence(TIME) == {
        "action": "presence",
        "time": str(TIME),
        "type": "status",
        "user": {
            "account_name": "Гость",
            "status": "Тут!"
        }
    }


@pytest.mark.parametrize("time, name, expected_result",
                         [
                             (TIME, "Вася", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Вася",
                                     "status": "Тут!"
                                 }
                             }),
                             (TIME, "Vaspupiy", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Vaspupiy",
                                     "status": "Тут!"
                                 }
                             }),
                             (TIME, '123456', {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "123456",
                                     "status": "Тут!"
                                 }
                             })
                         ])
def test_create_presence_good_status_default(time, name, expected_result):
    assert create_presence(time, name) == expected_result


@pytest.mark.parametrize("time, status, expected_result",
                         [
                             (TIME, "На месте", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Гость",
                                     "status": "На месте"
                                 }
                             }),
                             (TIME, "online", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Гость",
                                     "status": "online"
                                 }
                             }),
                             (TIME, '123456', {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Гость",
                                     "status": "123456"
                                 }
                             })
                         ])
def test_create_presence_good_name_default(time, status, expected_result):
    assert create_presence(time, status=status) == expected_result


@pytest.mark.parametrize("time, name, status, expected_result",
                         [
                             (TIME, "Вася", "На месте", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Вася",
                                     "status": "На месте"
                                 }
                             }),
                             (TIME, "Vaspupiy", "online", {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "Vaspupiy",
                                     "status": "online"
                                 }
                             }),
                             (TIME, "123", '123456', {
                                 "action": "presence",
                                 "time": str(TIME),
                                 "type": "status",
                                 "user": {
                                     "account_name": "123",
                                     "status": "123456"
                                 }
                             })
                         ])
def test_create_presence_good_no_default(time, name, status, expected_result):
    assert create_presence(time, name, status) == expected_result


def test_create_presence_good_type():
    assert type(create_presence(TIME, "Vaspupiy", "online")) == dict


def test_dumps_message_type():
    assert type(dumps_message({
        "action": "leave",
        "time": "12:00",
        "room": "room"
    })) == bytes


def test_send_message():
    # Не знаю, есть ли в этом смысл...
    s_serv = socket(AF_INET, SOCK_STREAM)
    s_serv.bind(('0.0.0.0', 7777))
    s_serv.listen(1)

    s_cl = socket(AF_INET, SOCK_STREAM)
    s_cl.connect(('localhost', 7777))

    client, addr = s_serv.accept()

    send_message(s_cl, 'abc'.encode())

    client.settimeout(1.0)
    msg_b = client.recv(1024)
    assert msg_b
    client.close()
    s_cl.close()
    s_serv.close()


def test_receive_message():
    s_serv = socket(AF_INET, SOCK_STREAM)
    s_serv.bind(('0.0.0.0', 7777))
    s_serv.listen(1)

    s_cl = socket(AF_INET, SOCK_STREAM)
    s_cl.connect(('localhost', 7777))

    client, addr = s_serv.accept()

    client.send('abc'.encode())
    msg = receive_message(s_cl, 1024)
    assert msg == 'abc'.encode()
    client.close()
    s_cl.close()
    s_serv.close()


@pytest.mark.parametrize("resp_message", [
    (
            {
                "response": 200,
                "alert": 'сообщение сервера'
            }
    ),
    (
            {
                "response": 400,
                "alert": 'другое сообщение сервера'
            }
    ),
    (
            {
                "response": 500,
                "alert": 'вот такое сообщение сервера'
            }
    )
]
                         )
def test_pars_message(resp_message):
    bytes_message = pickle.dumps(resp_message)
    assert parse_message(bytes_message) == resp_message


# не знаю как тестировать, всегда падает с ошибкой SystemExit!!!
def test_get_args_good(crutch_for_terminal_input_function):
    assert get_args('localhost', 7777, ).addr == 'localhost'
    assert get_args('localhost', 7777, ).port == 7777


def test_set_socket_connection():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('0.0.0.0', 7777))
    s.listen(1)
    assert (set_socket_connection('localhost', 7777))
    client, addr = s.accept()
    client.close()
    s.close()


# По итогам ...
def test_main():
    s_serv = socket(AF_INET, SOCK_STREAM)
    s_serv.bind(('0.0.0.0', 7777))
    s_serv.listen(1)
    assert main('localhost', 7777, datetime.now(), 1024, True) is None

import logging

import pytest
from log.server_log_config import init_logger as init_server_log

from log.client_log_config import init_logger as init_client_log


@pytest.fixture()
def crutch_for_terminal_input_function():
    import sys
    sys.argv = ['']
    del sys


@pytest.fixture()
def create_logger_server():
    if not logging.getLogger('tcp_server_log').handlers:
        init_server_log('tcp_server_log')
        _logger = logging.getLogger('tcp_server_log')
    else:
        _logger = logging.getLogger('tcp_server_log')
    return _logger


@pytest.fixture()
def create_logger_client():
    if not logging.getLogger('tcp_client_log').handlers:
        init_client_log('tcp_client_log')
        _logger = logging.getLogger('tcp_client_log')
    else:
        _logger = logging.getLogger('tcp_client_log')
    return _logger

import pytest


@pytest.fixture()
def crutch_for_terminal_input_function():
    import sys
    sys.argv = ['']
    del sys

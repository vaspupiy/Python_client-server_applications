"""
2. В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная.
Если имеется такой код:
@log
def func_z():
 pass

def main():
 func_z()
...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"
"""
import inspect
import logging
from functools import wraps


def log(func):
    format_logger = "%(asctime)s :: %(message)s"
    logger = logging.getLogger('lesson_6_task_2')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(
        filename='lesson_6_task_2.log',
        encoding='utf-8'
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(format_logger))
    logger.addHandler(fh)

    @wraps(func)
    def call(*args, **kwargs):
        cur_fr = inspect.currentframe()
        cal_fr = cur_fr.f_back
        cod_obj = cal_fr.f_code
        code_obj_name = cod_obj.co_name  # Гугл рулит!
        logger.debug(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return func(*args, **kwargs)

    return call


@log
def func_z():
    pass


def main():
    func_z()


main()

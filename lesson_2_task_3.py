import os
import yaml

"""
3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""


def save_yaml_data(_data: dict, _path: str, _encoding: str, _file_name='data'):
    os.makedirs(_path, exist_ok=True)
    path = os.path.join(_path, f'{_file_name}.yaml')
    with open(path, 'w', encoding=_encoding) as file:
        yaml.dump(_data, file, default_flow_style=False)


def see_yaml_file(_path: str, _encoding: str, _file_name='data'):
    path = os.path.join(_path, f'{_file_name}.yaml')
    with open(path, encoding=_encoding) as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    print(content)


if __name__ == '__main__':
    ENCODING = 'utf-8'
    DATA_FOLDER_PATH = 'task_3_date'
    DATA_FOR_WRITE = {
        'key_1': ['str_1', 1, []],
        'key_2': 14,
        'key_3': {
            'Наушники Эмоджи': '\U0001F3A7',
            'Перец чили': '\U0001F336',
            'Глаза Эмоджи': '\U0001F440',
            'Серп и молот': '\U0000262D'
        }
    }

    save_yaml_data(DATA_FOR_WRITE, DATA_FOLDER_PATH, ENCODING)
    see_yaml_file(DATA_FOLDER_PATH, ENCODING)

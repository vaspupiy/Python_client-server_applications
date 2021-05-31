import json
import os

"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""


def write_order_to_json(data_folder_path: str, file_name: str, encoding='utf-8', **kwargs):
    path = os.path.join(data_folder_path, f'{file_name}.json')
    with open(path, encoding=encoding) as file:
        dict_data = json.load(file)
    with open(path, 'w', encoding=encoding) as file:
        dict_data['orders'].append(kwargs)
        json.dump(dict_data, file, indent=4)


if __name__ == '__main__':
    DATA_FOLDER_PATH = 'task_2_date'
    DATA_FILE_NAME = 'orders'
    DATA_DICT = {
        'item': 'стол',
        'quantity': 14,
        'price': 153.43,
        'buyer': 'Клинет Петрович',
        'date': '30.05.2021'}

    write_order_to_json(DATA_FOLDER_PATH, DATA_FILE_NAME,  **DATA_DICT)

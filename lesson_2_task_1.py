import csv
import os
import re

"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например,
main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""


def test_csv_file(_file_path, _encoding):
    with open(_file_path, 'r', encoding=_encoding) as file:
        print(file.read())


def read_file(path_file, enc):
    with open(path_file, 'r', encoding=enc) as file:
        for line in file.readlines():
            yield line.strip()


def gen_data_files(data_path, _path, _encode):
    for file in _path:
        path = os.path.join(data_path, file)
        data_file = read_file(path, _encode)
        yield data_file


def create_main_data(data_path, _name_files, encode) -> list:
    lists_data = {  # По условию задания создаем 4-е списка, не куда не выводим и ни где не используем
        'os_prod_list': [],
        'os_name_list': [],
        'os_code_list': [],
        'os_type_list': [],
    }
    main_data = [
        ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    ]
    items_data = gen_data_files(data_path, _name_files, encode)
    for item in items_data:
        append_list = [None, None, None, None]
        for line in item:
            if main_data[0][0] in line:
                # tmp = line.split(':')[1]
                tmp = re.sub(r'.*:\s+', '', line)  # по условию извлекаем с помощью регулярных выражений
                lists_data['os_prod_list'].append(tmp)
                append_list[0] = tmp
            elif main_data[0][1] in line:
                # tmp = line.split(':')[1]
                tmp = re.sub(r'.*:\s+', '', line)
                lists_data['os_name_list'].append(tmp)
                append_list[1] = tmp
            elif main_data[0][2] in line:
                # tmp = line.split(':')[1]
                tmp = re.sub(r'.*:\s+', '', line)
                lists_data['os_code_list'].append(tmp)
                append_list[2] = tmp
            elif main_data[0][3] in line:
                # tmp = line.split(':')[1]
                tmp = re.sub(r'.*:\s+', '', line)
                lists_data['os_type_list'].append(tmp)
                append_list[3] = tmp
        main_data.append(append_list)
    # print(lists_data)  # по условию выводить не просили
    return main_data


def get_data(data_path, encode):
    name_files = os.listdir(data_path)
    main_data = create_main_data(data_path, name_files, encode)
    return main_data


def write_to_csv(_data, _folder_path, _encoding):
    os.makedirs(_folder_path, exist_ok=True)
    _file_path = os.path.join(_folder_path, 'main_data.csv')
    with open(_file_path, 'w', encoding=_encoding) as data_f:
        data_f_writer = csv.writer(data_f, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        for row in _data:
            data_f_writer.writerow(row)


if __name__ == '__main__':
    ENCODING = 'cp1251'
    DATA_PATH_RECEIVE = 'task_1_data_receive'
    DATA_PATH_SEND = 'task_1_data_send'

    data = get_data(DATA_PATH_RECEIVE, ENCODING)
    write_to_csv(data, DATA_PATH_SEND, ENCODING)
    file_path = os.path.join(DATA_PATH_SEND, 'main_data.csv')
    test_csv_file(file_path, ENCODING)

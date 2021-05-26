"""
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить
кодировку файла по умолчанию. Принудительно открыть файл в
формате Unicode и вывести его содержимое
"""

LINES = ["сетевое программирование", "сокет", "декоратор"]

with open('test_file.txt', 'w') as f:  # кодировка файла по умолчанию
    for line in LINES:
        f.write(line)
        f.write('\n')
    print(f)  # <_io.TextIOWrapper name='test_file.txt' mode='w' encoding='cp1251'>

with open('test_file.txt', 'r', encoding='utf-8', errors='replace') as f:
    print(f.read())

    """
    ������� ����������������
    �����
    ���������
    """
# # _______________________________________________________________________
# # Если я не правильно понял задание и все должно работать
#
# with open('test_file.txt', 'w', encoding='utf-8') as f:  # кодировка 'utf-8'
#     for line in LINES:
#         f.write(line)
#         f.write('\n')
#     print(f)  # <_io.TextIOWrapper name='test_file.txt' mode='w' encoding='utf-8'>
#
# with open('test_file.txt', 'r', encoding='utf-8') as f:
#     print(f.read())
#
# # _______________________________________________________________________
# #  Или можно попробовать все кодировки, которы +- должны подойти
# ENCODINGS = [
#     'utf-8',
#     'utf-16',
#     'ascii',
#     'cp1251',
#     'cp866',
# ]
#
# with open('test_file.txt', 'w') as f:  # кодировка файла по умолчанию
#     for line in LINES:
#         f.write(line)
#         f.write('\n')
#
# for encoding in ENCODINGS:
#     try:
#         with open('test_file.txt', 'r', encoding=encoding) as f:
#             print(f.read())
#     except (UnicodeDecodeError, UnicodeError):
#         pass
#
# #  Так прокатило и с 'cp1251'и 'cp866', а значит тоже не годится
#
# # _______________________________________________________________________
# #  Нагугленный способ:
# from chardet.universaldetector import UniversalDetector
#
# with open('test_file.txt', 'w') as f:  # кодировка файла по умолчанию
#     for line in LINES:
#         f.write(line)
#         f.write('\n')
#
# det = UniversalDetector()
# with open('test_file.txt', 'rb') as f:
#     for line in f:
#         det.feed(line)
#         if det.done:
#             break
#     det.close()
# print(det.result) #  {'encoding': 'windows-1251', 'confidence': 0.9929305516756276, 'language': 'Russian'}
# enc = det.result['encoding']
#
# with open('test_file.txt', 'r', encoding=enc) as f:
#     print(f.read())
#
# # хотя по условию "Принудительно открыть файл в формате Unicode и вывести его содержимое" , значит тоже не подходит

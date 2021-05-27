"""
Определить, какие из слов
«attribute», «класс», «функция», «type»
невозможно записать в байтовом типе.
"""


def is_write_in_bytes(_word):
    try:
        bytes(_word, 'ASCII')
    except UnicodeEncodeError:
        print(f'слово: "{_word}" не возможно записать в байтовом типе')


if __name__ == '__main__':
    WORLDS = ['attribute', 'класс', 'функция', 'type']
    for world in WORLDS:
        is_write_in_bytes(world)

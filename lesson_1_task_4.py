"""
Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
"""


def type_test(*args):
    for item in args:
        print(item, type(item))


if __name__ == "__main__":
    WORLDS = ['разработка', 'администрирование', 'protocol', 'standard']

    enc_worlds = [world.encode('utf-8') for world in WORLDS]
    print('\nрезультат преобразования в байтовое представление: ')
    type_test(*enc_worlds)

    dec_worlds = [world.decode('utf-8') for world in enc_worlds]
    print('\nрезультат преобразования в стороковое представление: ')
    type_test(*dec_worlds)

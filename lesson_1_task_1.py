"""
Каждое из слов «разработка», «сокет», «декоратор» представить в
строковом формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат
Unicode и также проверить тип и содержимое переменных.
"""

if __name__ == '__main__':

    WORLDS = {
        'разработка': '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
        'сокет': '\u0441\u043e\u043a\u0435\u0442',
        'декоратор': '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440',
    }

    for string_rep, unicode_rep in WORLDS.items():
        print(f'строковый формат слова: "{string_rep}" имеет тип: {type(string_rep)}')
        print(f'формат Unicode слова: "{unicode_rep}" имеет тип: {type(unicode_rep)}')

"""
Каждое из слов «class», «function», «method» записать в байтовом
типе без преобразования в последовательность кодов (не
используя методы encode и decode) и определить тип, содержимое
 и длину соответствующих переменных.
"""
if __name__ == '__main__':
    WORLDS = ['class', 'function', 'method']
    worlds_b = [bytes(world, 'ASCII') for world in WORLDS]
    for world_b in worlds_b:
        print(f'тип: {type(world_b)}, содержимое: {world_b}, длина: {len(world_b)}')


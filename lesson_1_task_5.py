"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import subprocess

if __name__ == "__main__":
    SITES = ['yandex.ru', 'youtube.com']
    for site in SITES:
        print(f'\nпинг веб-ресурса: {site}')
        args = ['ping', site]
        subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in subproc_ping.stdout:
            line = line.decode('cp866').encode('utf-8')
            print(line.decode('utf-8'))

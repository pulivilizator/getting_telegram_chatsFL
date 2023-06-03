import time

from get_chats.parsing_chats import main
if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex, ex.__doc__, ex.args)
    print('Сбор данных завершен')
    while True: time.sleep(5000)
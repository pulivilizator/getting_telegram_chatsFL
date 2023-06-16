from pyrogram import Client
from pyrogram.errors import FloodWait, MsgIdInvalid, RPCError

import asyncio
import configparser
import re
from itertools import cycle

from get_chats.handlers import _chek_entities, _pattern, _main_handler
from excel_writer.writer import writer


async def _get_messages(app: Client, settings: configparser.ConfigParser, chat, links):
    counter = settings.getint('program', 'message_count')

    async def async_generator():
        c = 1
        async for message in app.get_chat_history(chat):
            c += 1
            print(c, chat)
            if c == counter:
                break
            try:
                if message.entities:
                    async for url in _chek_entities(message):
                        if url:
                            yield _pattern(url)
                if message.text:
                    if _pattern(message.text):
                        yield _pattern(message.text)
                elif message.caption:
                    if _pattern(message.caption):
                        yield _pattern(message.caption)
            except MsgIdInvalid:
                pass

            except FloodWait as wait:
                print(f'FlooWait: {wait.value}')
                await asyncio.sleep(wait.value)

    async for i in async_generator():
        if i:
            for k in re.sub(r'(https://t\.me/(joinchat/)?(.+?))+', r' \3', ''.join(i)).split():
                if k[0] != '+':
                    links.add(k)


async def main():
    writer.create_file()
    settings = configparser.ConfigParser()
    settings.read('config.ini', encoding='utf-8')
    apps = cycle([(Client(f'session_{i}'), i) for i in range(1, settings.getint('program', 'sessions'))])
    chats = writer.get_rows()
    for chat in chats:
        links = set()
        final_chats = set()
        app, num = next(apps)
        try:
            await app.start()
        except ConnectionError:
            pass
        try:
            await _get_messages(app, settings, chat, links)
        except (RPCError, KeyError, ValueError, ConnectionError):
            continue
        c = 0
        for link in links:
            try:
                if len(final_chats) >= 100:
                    await writer.writer(final_chats)
                print(f'{num} - № аккаунта')
                c += 1
                print(f'{c} из {len(links)} ссылок проверено')

                await _main_handler(app, link, final_chats, chat)
                if settings.getboolean('program', 'waiter'):
                    await asyncio.sleep(settings.getint('program', 'wait'))
            except FloodWait as wait:
                print(f'FlooWait: {wait.value} сек')
                await app.stop()
                app, num = next(apps)
                try:
                    await app.start()
                    print('Меняю аккаунт')
                except:
                    pass
            except (RPCError, KeyError, ValueError, ConnectionError):
                continue

        await writer.writer(final_chats)
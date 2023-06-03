import time
from pyrogram import Client
from get_chats.handlers import _chek_entities, _pattern, _main_handler
from pyrogram.errors import FloodWait, MsgIdInvalid, RPCError
import asyncio
from excel_writer.writer import writer
from config.config import get_config
import configparser
import re


async def _get_messages(app: Client, settings: configparser.ConfigParser, chat, links, final_chats):
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
    c = 0
    for link in links:
        try:
            time.sleep(settings.getint('program', 'wait'))
            c += 1
            print(f'{c} из {len(links)} ссылок проверено')
            await _main_handler(app, link, final_chats, settings)
        except Exception:
            continue

    for m in final_chats:
        if chat not in m[0]:
            await writer.writer(m)
    settings.set('program', 'wait', '3')


def main():
    writer.create_file()
    settings = configparser.ConfigParser()
    settings.read('config.ini')
    chats = writer.get_rows()
    config = get_config(settings.get('program', 'env'))
    proxy = {
        "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
        "hostname": "194.28.210.240",
        "port": 9111,
        "username": "o4tdKM",
        "password": "NPSzJu"
    }
    app = Client('session', api_id=config.api_id, api_hash=config.api_hash, proxy=proxy)
    with app:
        for chat in chats:
            links = set()
            final_chats = []
            app.run(_get_messages(app, settings, chat, links, final_chats))

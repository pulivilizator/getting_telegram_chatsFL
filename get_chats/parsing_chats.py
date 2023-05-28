from pyrogram import Client
from get_chats.handlers import _chek_entities, _count_members_in_chat, _pattern
from pyrogram.errors import FloodWait, MsgIdInvalid
import asyncio
from excel_writer.writer import writer
from config.config import get_config
import configparser
import re


async def _get_messages(app: Client, settings: configparser.ConfigParser, chat):
    links = set()
    counter = settings.getint('program', 'message_count')

    async def async_generator():
        c = 1
        async for message in app.get_chat_history(chat):
            print(chat)
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
                links.add(k)
    await writer.writer(_count_members_in_chat(app, links))


async def main():
    writer.create_file()
    settings = configparser.ConfigParser()
    settings.read('config.ini')
    chats = writer.get_rows()
    config = get_config(settings.get('program', 'env'))
    app = Client('session', api_id=config.api_id, api_hash=config.api_hash)
    tasks = []
    async with app:
        for chat in ['bookSurfing',
                     'IgorLinkChannel',
                     'travelask_all_chats',
                     'jesusavgntwitch',
                     'nats_py',
                     'moikanaly2022',
                     'python_parsing',
                     'aiogram_dialog',
                     'kanaly'
                     ]:  # chats:
            task = asyncio.create_task(_get_messages(app, settings, chat))
            tasks.append(task)
        await asyncio.gather(*tasks)

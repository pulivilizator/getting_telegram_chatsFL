import configparser
import time
from langdetect import detect
from collections import defaultdict
from langdetect.lang_detect_exception import LangDetectException
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors import FloodWait, MsgIdInvalid, UsernameNotOccupied, UsernameInvalid, ChatAdminRequired
import re

async def _main_handler(app: Client, chat, final_chats, settings: configparser.ConfigParser):
    global chat_type
    lang_dict = defaultdict(int)
    c = 0
    try:
        async for i in app.get_chat_history(chat):
            c += 1
            if c == 80:
                break
            if i.text:
                lang_dict[detect(i.text)] += 1
                chat_type = str(i.chat.type)
            if i.caption:
                lang_dict[detect(i.caption)] += 1
                chat_type = str(i.chat.type)
        if lang_dict:
            counter = await _chat_check_members(app, chat, chat_type)
            if counter and counter >= 100:
                final_chats.append([f'https://t.me/{chat}', counter, max(lang_dict.items(), key=lambda x: x[1])[0], ])
    except (MsgIdInvalid, UsernameNotOccupied, ValueError, UsernameInvalid, LangDetectException) as ex:
        return -1
    except FloodWait as wait:
        print(f'FlooWait: {wait.value} сек')
        time.sleep(wait.value)
        wait_now = settings.getint('program', 'wait')
        settings.set('program', 'wait', str(wait_now + 1))


async def _chat_check_members(app: Client, chat: str, chat_type: str):
    c = 1
    try:
        count = await app.get_chat(chat)
        if chat_type in ('ChatType.GROUP', 'ChatType.SUPERGROUP'):
            async for _ in app.get_chat_members(chat):
                c += 1
            if c >= 100:
                return count.members_count
        else:
            return count.members_count
    except ChatAdminRequired:
        return 'Нет доступа'

def _pattern(text):
    return list(map(lambda x: x.group(), re.finditer(r'\bhttps://t\.me/(joinchat/)?.{4,}?\b', text)))


async def _chek_entities(message: Message):
    if message.entities:
        for i in message.entities:
            yield i.url
    if message.caption_entities:
        for i in message.caption_entities:
            yield i.url



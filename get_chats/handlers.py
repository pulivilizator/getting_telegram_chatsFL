import configparser
import asyncio
from langdetect import detect
from collections import defaultdict
from langdetect.lang_detect_exception import LangDetectException
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors import MsgIdInvalid, UsernameNotOccupied, UsernameInvalid, ChatAdminRequired
import re

async def _main_handler(app: Client, chat, final_chats, first_chat):
    global chat_type, counter
    lang_dict = defaultdict(int)
    c = 0
    try:
        async for i in app.get_chat_history(chat, limit=90):
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
            counter = await _chat_check_members(app, chat)
            chat_type = 'Группа' if chat_type in ('ChatType.GROUP', 'ChatType.SUPERGROUP') else 'Канал'
            if counter and counter >= 100:
                final_chats.add((f'https://t.me/{chat}', counter, max(lang_dict.items(), key=lambda x: x[1])[0], chat_type, f'@{first_chat}'))
    except (MsgIdInvalid, UsernameNotOccupied, UsernameInvalid, LangDetectException):
        return -1


async def _chat_check_members(app: Client, chat: str):
    try:
        count = await app.get_chat(chat)
        return count.members_count
    except ChatAdminRequired:
        return 0

def _pattern(text):
    return list(map(lambda x: x.group(), re.finditer(r'\bhttps://t\.me/(joinchat/)?.{4,}?\b', text)))


async def _chek_entities(message: Message):
    if message.entities:
        for i in message.entities:
            yield i.url
    if message.caption_entities:
        for i in message.caption_entities:
            yield i.url


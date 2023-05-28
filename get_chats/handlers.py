from langdetect import detect
from collections import defaultdict
from langdetect.lang_detect_exception import LangDetectException
from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message
from pyrogram.errors import FloodWait, MsgIdInvalid, UsernameNotOccupied, UsernameInvalid
import asyncio
import re


async def _lang_detecting(app: Client, chat):
    lang_dict = defaultdict(int)
    async for i in app.get_chat_history(chat, limit=50):
        if i.text:
            try:
                lang_dict[detect(i.text)] += 1
            except LangDetectException:
                pass
        if i.caption:
            try:
                lang_dict[detect(i.caption)] += 1
            except LangDetectException:
                pass
    if lang_dict:
        return max(lang_dict.items(), key=lambda x: x[1])[0]


async def _count_members_in_chat(app: Client, chats) -> list:
    for chat in chats:
        try:
            country = await _lang_detecting(app, chat)
            channel_type = await app.get_chat(chat)
            if str(channel_type.type) == 'ChatType.SUPERGROUP':
                counter_members = 0
                async for _ in app.get_chat_members(chat):
                    counter_members += 1
                    if counter_members > 100:
                        c = await app.get_chat_members_count(chat)
                        yield [f'https://t.me/{chat}', c, country]
                        break

            elif str(channel_type.type) == 'ChatType.CHANNEL':
                c = await app.get_chat_members_count(chat)
                if c > 100:
                    yield [f'https://t.me/{chat}', c, country]
        except (MsgIdInvalid, UsernameNotOccupied):
            continue

        except FloodWait as wait:
            print(f'FlooWait: {wait.value} сек')
            await asyncio.sleep(wait.value)

        except ValueError:
            print('ERROR', chat)
            continue

        except UsernameInvalid:
            continue


def _pattern(text):
    return list(map(lambda x: x.group(), re.finditer(r'\bhttps://t\.me/(joinchat/)?.{4,}?\b', text)))


async def _chek_entities(message: Message):
    if message.entities:
        for i in message.entities:
            yield i.url
    if message.caption_entities:
        for i in message.caption_entities:
            yield i.url

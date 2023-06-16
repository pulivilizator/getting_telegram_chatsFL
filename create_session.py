import asyncio

from pyrogram import Client, filters
import dataclasses
from environs import Env, EnvError
from exceptions import *


@dataclasses.dataclass
class TgSession:
    session_name: str
    api_id: int
    api_hash: str


def get_config(path=None) -> TgSession:
    try:
        env = Env()
        env.read_env(path)
    except EnvError:
        raise EnvException('Ошибка считывания окружения')

    return TgSession(session_name=env('SESSION_NAME'), api_id=int(env('API_ID')), api_hash=env('API_HASH'))


async def creator():
    config = get_config()
    app = Client(config.session_name, api_id=config.api_id, api_hash=config.api_hash)
    await app.start()
    await app.stop()

if __name__ == '__main__':
    asyncio.run(creator())
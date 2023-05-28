import dataclasses
from environs import Env, EnvError
from exceptions import *


@dataclasses.dataclass
class TgSession:
    api_id: int
    api_hash: str


def get_config(path=None) -> TgSession:
    try:
        env = Env()
        env.read_env(path)
    except EnvError:
        raise EnvException('Ошибка считывания окружения')

    return TgSession(api_id=int(env('API_ID')), api_hash=env('API_HASH'))
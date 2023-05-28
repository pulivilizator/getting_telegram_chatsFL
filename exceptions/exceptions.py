class CreateSessionException(Exception):
    """Ошибка создания сессии"""

class EnvException(Exception):
    """Обишка считывания окружения"""

class GetFileException(Exception):
    """Ошибка считывания файла на входе(файл не найден)"""


class WriteFileException(Exception):
    """Ошибка записи в файл(файл не найден)"""


class CreateFileException(Exception):
    """Ошибка создания файла"""

class GetUserDataException(Exception):
    """Ошибка обработки/получения данных пользователя"""


from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message

from Bot.google_doc.googleSheets import get_active_user


class UserIsActive(BaseFilter):
    def __init__(self, revers: bool = False, *args, **kwargs):
        """
        :param revers: фильтр на наличие(False) или отсутствие(True)
        :return: None"""
        self.revers = revers

    # , command: CommandObject
    async def __call__(self, mess: Message) -> bool:
        if self.revers:
            return not (str(mess.from_user.id) in get_active_user())
        return str(mess.from_user.id) in get_active_user()

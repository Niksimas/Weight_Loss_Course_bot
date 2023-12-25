from aiogram.filters import BaseFilter
from aiogram.types import Message

from Bot.BD.work_db import check_activity_user


class UserIsActive(BaseFilter):
    def __init__(self, *args, **kwargs):
        pass

    async def __call__(self, mess: Message) -> bool:
        return check_activity_user(str(mess.from_user.id))

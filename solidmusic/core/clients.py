from __future__ import annotations
from pyrogram import Client
from pyrogram.types import User
from pytgcalls import PyTgCalls
from configs import config
from typing import Any, Iterable


class Client(RawClient):
    def __init__(self, **kwargs: Any):
        self._me: User | None = None
        super().__init__(**kwargs)

    async def get_me(self, cached: bool = True) -> User:
        if not cached or self._me is None:
            self._me = await super().get_me()

        return self._me

    async def start(self):
        await super().start()
        self._me = await self.get_me()

    async def get_username(self) -> str | None:
        return (await self.get_me()).username

    async def get_full_name(self) -> str:
        me = await self.get_me()
        return f"{me.first_name} {me.last_name or ''}"

    async def mention(self, user_ids: Iterable[int | str] | str | int) -> str:
        return (await super().get_users(user_ids)).mention


user = Client(
    name="userbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION,
)

bot = Client(
    name=":memory:",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins={"root": "solidmusic.plugins"},
)

call_py = PyTgCalls(user)

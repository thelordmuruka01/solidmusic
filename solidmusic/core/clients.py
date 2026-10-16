from pyrogram import Client
from pytgcalls import PyTgCalls
from configs import config


user = Client(
    "userbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.SESSION,
)


bot = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins={"root": "solidmusic.plugins"},
)

call_py = PyTgCalls(user)

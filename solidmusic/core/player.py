
import sys
from pathlib import Path
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import idle
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import CallbackQuery
from configs import config
from .calls import leave_from_inactive_call
from .telegram_call import TelegramPlayer
from .youtube_call import YoutubePlayer
from solidmusic.core import username as usernames
from solidmusic.plugins import load_module


username = usernames
scheduler = AsyncIOScheduler()


class MediaPlayer(TelegramPlayer, YoutubePlayer):
    async def join_call(
        self,
        stream_type: str,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
    ):
        if stream_type == "music":
            await self.play(
                cb, user_id, title, duration, yt_url, yt_id
            )
        elif stream_type == "video":
            await self.video_play(
                cb, user_id, title, duration, yt_url, yt_id
            )

    async def music_or_video(self, cb: CallbackQuery, result: Dict):
        user_id = int(result["user_id"])
        title = result["title"]
        duration = result["duration"]
        yt_url = result["yt_url"]
        yt_id = result["yt_id"]
        stream_type = result["stream_type"]

        await self.join_call(
            stream_type,
            cb,
            user_id,
            title,
            duration,
            yt_url,
            yt_id,
        )

    async def run(self):
        try:
            self.db.init()

            print("[+] START BOT CLIENT")
            await self.bot.start()
            await self.user.start()

            print("[+] LOAD ALL MODULES")
            load_module()

            print("[+] GETTING BOT USERNAME")
            bot_me = await self.bot.get_me()
            bot_username = bot_me.username

            print(f"[+] Bot Username: {bot_username}")

            # Update the shared username value.
            usernames = bot_username

            print("[+] START PyTgCalls CLIENT")
            await self.call.start()

            try:
                await self.user.join_chat("HQ_Tracks")
            except UserAlreadyParticipant:
                pass

            print("[+] CLIENT RUNNING")
            await idle()

        finally:
            print("[+] STOPPING BOT")

            # Stop the call client if it was initialized.
           
            for directory in ("downloads", "image"):
                path = Path(directory)
                if path.exists() and path.is_dir():
                    import shutil
                    shutil.rmtree(path)

        return


player = MediaPlayer()

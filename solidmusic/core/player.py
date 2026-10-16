
import asyncio
import shutil
from pathlib import Path
from typing import Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import idle
from pyrogram.errors import FloodWait, UserAlreadyParticipant
from pyrogram.types import CallbackQuery

from .calls import leave_from_inactive_call
from .telegram_call import TelegramPlayer
from .youtube_call import YoutubePlayer
from solidmusic.plugins import load_module
import solidmusic.core as core_module


scheduler = AsyncIOScheduler()


class MediaPlayer(TelegramPlayer, YoutubePlayer):

    async def start_bot_safely(self):
        try:
            await self.bot.start()
            return True

        except FloodWait as e:
            wait_seconds = int(e.value) + 5

            print(
                f"Telegram FLOOD_WAIT: waiting "
                f"{wait_seconds} seconds before one retry."
            )

            await asyncio.sleep(wait_seconds)

            try:
                await self.bot.start()
                return True

            except FloodWait as retry_error:
                print(
                    "Telegram login is still rate-limited. "
                    f"Telegram requires another "
                    f"{retry_error.value} seconds. "
                    "Stopping startup without another retry."
                )
                return False

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

            if not await self.start_bot_safely():
                return

            await self.user.start()

            print("[+] LOAD ALL MODULES")
            load_module()

            print("[+] GETTING BOT USERNAME")
            bot_me = await self.bot.get_me()
            bot_username = bot_me.username

            print(f"[+] Bot Username: {bot_username}")
            core_module.username = bot_username

            print("[+] START PyTgCalls CLIENT")
            await self.call.start()
            try:
                await self.user.join_chat("HQ_Tracks")
            except UserAlreadyParticipant:
                pass

            print("[+] CLIENT RUNNING")
            print("[+] Waiting for Telegram shutdown signals...")
            await idle()
            print("[!] idle() returned; checking why the bot is exiting.")
        finally:
            print("[+] STOPPING BOT")

            for directory in ("downloads", "image"):
                path = Path(directory)
                if path.exists() and path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)


player = MediaPlayer()

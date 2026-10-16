from asyncio import sleep

from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import CallbackQuery, Message
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

from functions.youtube_utils import get_audio_direct_link, get_video_direct_link
from database.lang_utils import get_message as gm
from .calls import Call


class YoutubePlayer(Call):
    async def _play(
        self,      
        chat_id: int,
        user_id: int,
        audio_url: str,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
    ):
        bot_username = (await self.bot.get_me()).username
        mention = await self.bot.get_user_mention(user_id)
        call = self.call
        playlist = self.playlist.playlist
        if playlist and chat_id not in playlist:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "music"
            )
        elif not playlist:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "music"
            )
        audio_quality, _ = self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioPiped(audio_url, audio_quality),
                stream_type=StreamType().local_stream,
            )
            return 
        except NoActiveGroupCall:
            await self.join_chat(chat_id)
            await self.start_call(chat_id)
            await self._play(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id
            )
        except FloodWait as Fw:           
            await sleep(Fw.x)
            await self._play(
                chat_id, user_id, audio_url, title, duration, yt_url, yt_id
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            await self._play(
                 chat_id, user_id, audio_url, title, duration, yt_url, yt_id
            )

    async def _video_play(
        self,      
        chat_id: int,
        user_id: int,
        video_url: str,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
    ):
        call = self.call
        playlist = self.playlist.playlist
        if playlist and chat_id not in playlist:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "video"
            )
        elif not playlist:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "video"
            )
        mention = await self.bot.get_user_mention(user_id)
        bot_username = (await self.bot.get_me()).username
        audio_quality, video_quality = self.get_quality(chat_id)
        try:
            await call.join_group_call(
                chat_id,
                AudioVideoPiped(video_url, audio_quality, video_quality),
                stream_type=StreamType().local_stream,
            )
            
        except NoActiveGroupCall:
            await self.join_chat(chat_id)
            await self.start_call(chat_id)
            await self._video_play(
                 chat_id, user_id, video_url, title, duration, yt_url, yt_id
            )
        except FloodWait as Fw:           
            await sleep(Fw.x)
            await self._video_play(
                 chat_id, user_id, video_url, title, duration, yt_url, yt_id
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            await self._video_play(
                 chat_id, user_id, video_url, title, duration, yt_url, yt_id
            )

    async def play(
        self,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
    ):
        playlist = self.playlist.playlist
        chat_id = cb.message.chat.id
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "music"
            )          
            await sleep(5)                  
        audio_url = get_audio_direct_link(yt_url)
        await self._play(
            chat_id, user_id, audio_url, title, duration, yt_url, yt_id
        )
    async def video_play(
        self,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
    ):
        chat_id = cb.message.chat.id
        playlist = self.playlist.playlist
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            self.init_youtube_player(
                chat_id, user_id, title, duration, yt_url, yt_id, "video"
            )          
            await sleep(5)                
        video_url = get_video_direct_link(yt_url)
        await self._video_play(
            chat_id, user_id, video_url, title, duration, yt_url, yt_id
        )

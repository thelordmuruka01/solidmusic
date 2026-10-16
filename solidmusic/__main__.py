
import asyncio
from os import path, mkdir

from health_server import start_health_server
from solidmusic.core.player import player


async def main():
    if not path.exists("search"):
        mkdir("search")

    start_health_server()
    await player.run()


if __name__ == "__main__":
    asyncio.run(main())

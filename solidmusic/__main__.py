
import asyncio
from os import path, mkdir

from health_server import start_health_server
from solidmusic.core.player import player


def main():
    if not path.exists("search"):
        mkdir("search")

    start_health_server()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(player.run())
    finally:
        loop.close()


if __name__ == "__main__":
    main()

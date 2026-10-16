import asyncio
from solidmusic.core.player import player
from os import path, mkdir
from health_server import start_health_server
from solidmusic.core.player import player

def main():
    if not path.exists("search"):
        mkdir("search")

    start_health_server()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(player.run())

main()

def main():
    if not path.exists("search"):
        mkdir("search")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(player.run())


main()

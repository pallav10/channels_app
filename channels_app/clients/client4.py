# Run ``pip install websockets`` before importing the library.
# !/usr/bin/env python3
from asyncio import gather, get_event_loop

import websockets
# The client is also as an asynchronous context manager.
from aioconsole import ainput


# establishes a connection / intantes the client.
# The client is actually an awaiting function that yields an
# object which can then be used to send and receive messages.


async def socket_func():
    connection = websockets.connect(uri="ws://127.0.0.1:8080/ws/rearrange/4")

    async def take_input():
        async with connection as websocket:
            # Sends a message.
            await websocket.send(await ainput())
            await print_message(take_new_input=True)

    async def print_message(take_new_input=False):
        async with connection as websocket:
            # Sends a message.

            # Receives the replies.
            if not take_new_input:
                async for message in websocket:
                    print(message)
            if take_new_input:
                await take_input()

    async def multiple():
        tasks = [take_input(), print_message()]
        await gather(*tasks)
        # Closes the connection.
        # await websocket.close()

    while True:
        await multiple()


def main():
    loop = get_event_loop()
    loop.run_until_complete(socket_func())
    loop.close()


if __name__ == "__main__":
    main()

# Run ``pip install websockets`` before importing the library.
# !/usr/bin/env python3
from asyncio import gather, get_event_loop

import websockets

# The client is also as an asynchronous context manager.
from aioconsole import ainput


# establishes a connection / instantiates the client.
# The client is actually an awaiting function that yields an
# object which can then be used to send and receive messages.


async def socket_func():
    connection = websockets.connect(uri="ws://127.0.0.1:8080/ws/rearrange/2")

    async def send_messages(websocket):
        # Sends a message.
        message = await ainput()
        if message in ["exit", "quit"]:
            await websocket.close()
        await websocket.send(message)
        await get_replies(websocket, take_new_input=True)

    async def get_replies(websocket, take_new_input=False):
        # Receives the replies.
        if not take_new_input:
            async for message in websocket:
                print(message)
        if take_new_input:
            await send_messages(websocket)

    async def multiple(websocket):
        tasks = [send_messages(websocket), get_replies(websocket)]
        await gather(*tasks)

    async with connection as websocket:
        await multiple(websocket)


def main():
    loop = get_event_loop()
    loop.run_until_complete(socket_func())
    loop.close()


if __name__ == "__main__":
    main()

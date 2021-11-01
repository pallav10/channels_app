# Run ``pip install websockets`` before importing the library.
# !/usr/bin/env python3
import asyncio

import websockets
from aioconsole import ainput


# establishes a connection / intantes the client.
# The client is actually an awaiting function that yields an
# object which can then be used to send and receive messages.

# The client is also as an asynchronous context manager.
async def socket_func():
    connection = websockets.connect(uri="ws://127.0.0.1:8080/ws/rearrange/1")
    async with connection as websocket:
        # Sends a message.
        await websocket.send(await ainput("Enter numbers separated by spaces: "))

        # Receives the replies.
        async for message in websocket:
            print(message)

        # Closes the connection.
        await websocket.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(socket_func())
    loop.close()


if __name__ == "__main__":
    main()

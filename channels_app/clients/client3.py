# Run ``pip install websockets`` before importing the library.
# !/usr/bin/env python3
import os
from asyncio import gather, get_event_loop

import websockets

# The client is also as an asynchronous context manager.
from aioconsole import ainput

from channels_app.encryption_util import Encryptor

# establishes a connection / instantiates the client.
# The client is actually an awaiting function that yields an
# object which can then be used to send and receive messages.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "duplex_sys.settings")


class WebSocketClient(object):
    def __init__(self):
        self.connection = websockets.connect(uri=f"ws://127.0.0.1:8080/ws/rearrange/3")
        self.encryptor = Encryptor()

    async def socket_func(self):
        async def send_messages(instance: WebSocketClient, websocket):
            # Sends a message.
            message = await ainput()
            if message in ["exit", "quit"]:
                await websocket.close()
            encrypted_message = instance.encryptor.encrypt(message)
            await websocket.send(encrypted_message)
            await get_replies(instance, websocket, take_new_input=True)

        async def get_replies(
            instance: WebSocketClient, websocket, take_new_input=False
        ):
            # Receives the replies.
            if not take_new_input:
                async for message in websocket:
                    decrypted_message = instance.encryptor.decrypt(message)
                    print(decrypted_message)
            if take_new_input:
                await send_messages(instance, websocket)

        async def multiple(instance: WebSocketClient, websocket):
            tasks = [
                send_messages(instance, websocket),
                get_replies(instance, websocket),
            ]
            await gather(*tasks)

        async with self.connection as websocket:
            await multiple(self, websocket)


def main():
    loop = get_event_loop()
    client = WebSocketClient()
    loop.run_until_complete(client.socket_func())
    loop.close()


if __name__ == "__main__":
    main()

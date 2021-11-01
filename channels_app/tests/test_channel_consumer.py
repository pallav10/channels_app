import json

import pytest

# Create your tests here.
from channels.routing import URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.testing import WebsocketCommunicator
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import path

from channels_app.consumer import RearrangeNumbersApp

TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


class SimpleWebsocketApp(RearrangeNumbersApp):
    """
    Barebones WebSocket ASGI app for testing.
    """

    pass


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
@pytest.mark.asyncio
class TestWebSocket(TestCase):
    def setUp(self) -> None:
        super(TestWebSocket, self).setUp()
        self.application = SessionMiddlewareStack(
            URLRouter(
                [path("ws/rearrange/<int:chat_id>", SimpleWebsocketApp.as_asgi())]
            )
        )
        cache.clear()

    def make_communicator(self, channel_id):
        return WebsocketCommunicator(
            application=self.application, path=f"/ws/rearrange/{channel_id}"
        )

    async def test_can_connect_to_server(self):
        communicator = self.make_communicator(1)
        connected, subprotocol = await communicator.connect()
        # Test connection
        assert connected
        assert subprotocol is None
        # Test sending text
        await communicator.send_to(text_data="1 2 3 4 5 6 7 8")
        response = await communicator.receive_from()
        response = json.loads(response)
        self.assertEqual(response, {"message": [1, 3, 2, 5, 4, 7, 6, 8]})
        # Close out
        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_can_multiple_connect_to_server_sequential(self):
        communicator1 = self.make_communicator(2)
        connected, subprotocol = await communicator1.connect()
        # Test connection
        assert connected
        assert subprotocol is None
        # Test sending text
        await communicator1.send_to(text_data="1 2 3 4 5 6 7 8")
        response1 = await communicator1.receive_from()
        response1 = json.loads(response1)
        self.assertEqual(response1, {"message": [1, 3, 2, 5, 4, 7, 6, 8]})

        # connect second communicator
        communicator2 = self.make_communicator(3)
        connected, subprotocol = await communicator2.connect()
        # Test connection
        assert connected
        assert subprotocol is None
        # Test sending text
        await communicator2.send_to(text_data="10 11 12 13 14 15 16 17 18")
        response2 = await communicator2.receive_from()
        response2 = json.loads(response2)
        self.assertEqual(response2, {"message": [10, 12, 11, 14, 13, 16, 15, 18, 17]})
        # Close out communicator1
        await communicator1.disconnect()
        await communicator2.disconnect()

    @pytest.mark.django_db
    @pytest.mark.asyncio
    async def test_can_multiple_connections_to_server_parallel(self):
        # connect first communicator
        communicator1 = self.make_communicator(4)
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)

        communicator2 = self.make_communicator(5)
        connected2, _ = await communicator2.connect()
        # Test connection
        self.assertTrue(connected2)

        # Test sending text out of order (for 2nd communicator first)
        await communicator2.send_to(text_data="10 11 12 13 14 15 16 17 18")
        response2 = await communicator2.receive_from()
        response2 = json.loads(response2)
        self.assertEqual(response2, {"message": [10, 12, 11, 14, 13, 16, 15, 18, 17]})

        # Test sending text for 1st communicator
        await communicator1.send_to(text_data="1 2 3 4 5 6 7 8")
        response1 = await communicator1.receive_from()
        response1 = json.loads(response1)
        self.assertEqual(response1, {"message": [1, 3, 2, 5, 4, 7, 6, 8]})

        # Close out communicator1
        await communicator1.disconnect()
        await communicator2.disconnect()

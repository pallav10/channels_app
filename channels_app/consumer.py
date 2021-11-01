# Built in imports.
import json

# Third Party imports.
from channels.generic.websocket import AsyncWebsocketConsumer

from channels_app.encryption_util import Encryptor


def swap(Arr, i, j):
    """
    Utility function to swap elements `A[i]` and `A[j]` in the list
    """
    temp = Arr[i]
    Arr[i] = Arr[j]
    Arr[j] = temp


def rearrange_array(A):
    """
    Function to rearrange the list such that every second element
    of the list is greater than its left and right elements
    """
    # start from the second element and increment index
    # by 2 for each iteration of the loop
    for i in range(1, len(A), 2):

        # if the previous element is greater than the current element,
        # swap the elements
        if A[i - 1] > A[i]:
            swap(A, i - 1, i)

        # if the next element is greater than the current element,
        # swap the elements
        if i + 1 < len(A) and A[i + 1] > A[i]:
            swap(A, i + 1, i)


class RearrangeNumbersApp(AsyncWebsocketConsumer):
    """
    Application that receives a string of space separated numbers, rearranges it in such a way,
     that every second element is greater than left and right element
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_id = None
        self.room_group_name = None
        self.encryptor = None

    async def connect(self):
        """
        handles every new connection
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.chat_id
        self.encryptor = Encryptor()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    # Receive message from WebSocket
    async def websocket_receive(self, message):
        """
        Receives messages from clients
        """
        # Send message to room group
        decrypted_message = self.encryptor.decrypt(message["text"])
        await self.receive(text_data=decrypted_message)

    async def disconnect(self, close_code):
        """
        Disconnects clients
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data="", bytes_data=None):
        """
        Receives message from clients processes it and send it back
        """
        list_of_numbers = list(sorted(map(int, text_data.split())))
        rearrange_array(list_of_numbers)
        message = json.dumps(dict(message=list_of_numbers))
        encrypted_message = self.encryptor.encrypt(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_rearranged",
                "message": encrypted_message,
            },
        )

    # Receive message from room group
    async def send_rearranged(self, event):
        """
        Sends back rearranged list of numbes
        """
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=message)

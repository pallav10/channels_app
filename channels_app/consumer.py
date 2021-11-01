# Built in imports.
import json

# Third Party imports.
from channels.generic.websocket import AsyncWebsocketConsumer


# Django imports.


# Local imports.
# Utility function to swap elements `A[i]` and `A[j]` in the list
def swap(Arr, i, j):
    temp = Arr[i]
    Arr[i] = Arr[j]
    Arr[j] = temp


# Function to rearrange the list such that every second element
# of the list is greater than its left and right elements
def rearrange_array(A):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = None
        self.room_group_name = None

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.chat_id

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    # Receive message from WebSocket
    async def websocket_receive(self, message):
        # Send message to room group
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.chat_id
        await self.receive(text_data=message["text"])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data="", bytes_data=None):
        list_of_numbers = list(sorted(map(int, text_data.split())))
        rearrange_array(list_of_numbers)
        message = json.dumps(dict(message=list_of_numbers))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_rearranged",
                "message": message,
            },
        )

    # Receive message from room group
    async def send_rearranged(self, event):
        message = event["message"]
        # Send message to WebSocket
        print(self.room_group_name)
        await self.send(text_data=message)

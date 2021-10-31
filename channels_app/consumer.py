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


class RearrangeNumbersConsumer(AsyncWebsocketConsumer):

    # Receive message from WebSocket
    async def websocket_receive(self, message):
        list_of_numbers = list(sorted(map(int, message.get("text", "").split())))
        rearrange_array(list_of_numbers)
        message = json.dumps(dict(rearranged_array=list_of_numbers))

        # Send message to room group
        await self.receive(text_data=message)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class RearrangeNumbersApp(RearrangeNumbersConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.chat_id

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await super(RearrangeNumbersConsumer, self).connect()

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=text_data, bytes_data=bytes_data, close=True)

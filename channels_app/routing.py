from channels.routing import URLRouter
from django.urls import path

from channels_app.consumer import RearrangeNumbersApp

websocket_urlpatterns = URLRouter(
    [
        path(
            "ws/rearrange/<int:chat_id>",
            RearrangeNumbersApp.as_asgi(),
            name="rearrange",
        ),
    ]
)

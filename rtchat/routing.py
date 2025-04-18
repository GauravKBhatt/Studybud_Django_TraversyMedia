from django.urls import path
from .consumers import *
# consumers.py is the views.py equivalent for the web sockets.

websocket_urlpatters = [
    path("ws/chatroom/<chatroom_name>",ChatroomConsumer.as_asgi()),
]
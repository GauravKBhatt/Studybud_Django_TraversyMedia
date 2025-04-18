from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import *
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        # the websocket does not have access to the request object thus, we use scope function to acess the data about the user.
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name = self.chatroom_name)
        self.accept()

    def receive(self, text_data):
        try:
            print(type(text_data))
            text_data_json = json.loads(text_data)
            print(type(text_data_json))
            body = text_data_json.get('body')

            if body:
                message = GroupMessage.objects.create(
                    body=body,
                    author=self.user,
                    group=self.chatroom
                )

                context={
                    'message':message,
                    'user':self.user,
                }
                html = render_to_string("rtchat/chat_message_partial.html", context=context)
                # self.send(text_data=html)
                # must wrap your html in thejson format
                self.send(text_data=json.dumps({
                'message':html
                }))
            
            else:
                self.send(text_data=json.dumps({
                    'error':'Message body is missing.'
                }))

        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                'error':'Invalid JSON data'
            }))
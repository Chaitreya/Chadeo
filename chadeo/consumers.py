import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data ):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message",
                "message": message,
                "username": user.username
            }
        )

    def chat_message(self,event):
        message = event["message"]
        username = event["username"]

        html = render_to_string("chadeo/partials/messages.html",{
            "message": message,
            "username": username
        })

        self.send(text_data=html)
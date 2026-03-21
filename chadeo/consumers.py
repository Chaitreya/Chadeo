import json
import grpc

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

# 1. Import your generated gRPC files
from . import signaling_pb2_grpc as signaling_pb2__grpc
from . import signaling_pb2 as signaling__pb2
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # 2. ACKNOWLEDGEMENT: Tell C++ that someone joined
        self.send_presence_to_cpp()


    def send_presence_to_cpp(self):
        """Sends a 'Hello' to the C++ Worker immediately on connection"""
        try:
            with grpc.insecure_channel('localhost:50051') as channel:
                stub = signaling_pb2__grpc.MediaSignalingStub(channel)
                
                # We send a dummy/initial SDP just to satisfy the .proto contract
                request = signaling__pb2.CallRequest(
                    room_id=self.room_name,
                    user_id=self.scope["user"].username,
                    sdp_offer="INIT_CONNECTION" 
                )

                # The actual call
                response = stub.InitiateCall(request)
                
                if response.success:
                    print(f"✅ C++ Ack: {self.room_name} is now active in the worker.")
                    print(response.sdp_answer)
        except grpc.RpcError as e:
            print(f"⚠️ C++ Worker not reachable: {e.code()}")

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
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from mychat.models import Message, UserCustom


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # await self.get_user_custom(self.scope["user"])
        user = await sync_to_async(UserCustom.objects.get)(id=1)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        await self.save_messages(user=user, message=message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    # @database_sync_to_async
    # def get_user(self):
    #     return self.scope["user"]

    @database_sync_to_async
    def add_user(user):
        return UserCustom.objects.create(user=user)

    @database_sync_to_async
    def get_user_custom(self, user):
        user = UserCustom.objects.get(id=1)
        return user if user else None

    @database_sync_to_async
    def del_user(user):
        return UserCustom.objects.get(user=user).delete()

    @database_sync_to_async
    def save_messages(self, user, message):
        return Message.objects.create(user=user, message=message)


# import json
#
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
#
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
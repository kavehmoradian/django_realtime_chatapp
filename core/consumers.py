from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from chat.models import Chat, Message
from accounts.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['username']
        self.group_name = f"chat_{self.user_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"
            sender = User.objects.get(username=text_data_json['sender'])
            receiver = User.objects.get(username=text_data_json['receiver'])
            chat_session = Chat.chat_session_exists(sender, receiver)
            text = text_data_json['text']
            Message.objects.create(text=text, sender=sender, chat=chat_session)

            async_to_sync(self.channel_layer.group_send)(
                user_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=message)

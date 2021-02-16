from .models import Room, Message
from account.models import User
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def init_chat(self, data):
        username = data['username']
        content = {
            'command': 'init_chat',
            'success': 'Chatting in with success with username: ' + username
        }
        self.send_message(content)

    def fetch_messages(self, data):
        room = Room.objects.get(id=data['room'])
        
        messages = Message.objects.filter(room=room)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        sender = data['from']
        content = data['text']
        roomid = data['room']
        user = User.objects.get(username=sender)
        room = Room.objects.get(id=roomid)
        message = Message.objects.create(sender=user, content=content, room=room)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': str(message.id),
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    commands = {
        'init_chat': init_chat,
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }
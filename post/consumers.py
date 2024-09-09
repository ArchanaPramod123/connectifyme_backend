import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        # Initialize room_group_name to avoid AttributeError in disconnect
        self.room_group_name = f'notify_{self.user.id}'
        
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({
                'status': 'connected'
            }))
    
    async def receive(self, text_data):
        await self.send(text_data=json.dumps({'status': 'Ok, received'}))

    async def disconnect(self, close_code):
        # Ensure room_group_name is always available
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Custom handler to send notifications
    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'payload': data
        }))

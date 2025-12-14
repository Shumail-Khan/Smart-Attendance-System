import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "monitoring connected"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)
        
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LiveFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "Connected to live feed"}))

    async def disconnect(self, close_code):
        print("Live feed disconnected")

    # Receive data from server (e.g., base64 frame)
    async def send_frame(self, event):
        frame = event["frame"]
        await self.send(text_data=json.dumps({"frame": frame}))


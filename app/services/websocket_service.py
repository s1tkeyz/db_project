import json
from typing import Dict, Set
from fastapi import WebSocket
from .notification_service import NotificationService

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            'flight_status': set(),
            'checkin': set(),
            'booking': set(),
            'gate_changes': set()
        }
        self.notification_service = NotificationService()

    async def connect(self, websocket: WebSocket, channel: str):
        """Подключает клиента к WebSocket"""
        await websocket.accept()
        if channel in self.active_connections:
            self.active_connections[channel].add(websocket)

    async def disconnect(self, websocket: WebSocket, channel: str):
        """Отключает клиента от WebSocket"""
        if channel in self.active_connections:
            self.active_connections[channel].remove(websocket)

    async def broadcast(self, channel: str, message: dict):
        """Отправляет сообщение всем подключенным клиентам канала"""
        if channel in self.active_connections:
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_json(message)
                except:
                    await self.disconnect(connection, channel)

    async def handle_redis_message(self, channel: str, message: dict):
        """Обрабатывает сообщение из Redis и отправляет его через WebSocket"""
        await self.broadcast(channel.split(':')[1], message)

    async def start_listening(self):
        """Начинает прослушивание Redis каналов"""
        channels = [
            self.notification_service.CHANNELS['flight_status'],
            self.notification_service.CHANNELS['checkin'],
            self.notification_service.CHANNELS['booking'],
            self.notification_service.CHANNELS['gate_changes']
        ]
        await self.notification_service.subscribe(channels, self.handle_redis_message) 
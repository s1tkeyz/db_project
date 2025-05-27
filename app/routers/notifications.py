from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.websocket_service import WebSocketManager

router = APIRouter(prefix="/ws")
manager = WebSocketManager()

@router.websocket("/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    """Endpoint для WebSocket подключений"""
    await manager.connect(websocket, channel)
    try:
        while True:
            # Ждем сообщений от клиента (если нужно)
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket, channel)

# Запускаем прослушивание Redis каналов при старте приложения
@router.on_event("startup")
async def startup_event():
    await manager.start_listening() 
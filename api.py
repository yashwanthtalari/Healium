import os
import sys
import json
import asyncio
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# WebSocket Manager to handle multiple GUI connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Handle stale connections
                pass

manager = ConnectionManager()

# LogStream to capture stdout and send to GUI
class LogStream:
    def __init__(self):
        self.original_stdout = sys.stdout
        sys.stdout = self

    def write(self, data):
        self.original_stdout.write(data)
        if data.strip():
            # Send to all connected GUI clients
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        manager.broadcast({"type": "log", "data": data.strip()}), 
                        loop
                    )
            except Exception:
                pass

    def flush(self):
        self.original_stdout.flush()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Serve the GUI
@app.get("/")
async def get_gui():
    return FileResponse("gui/index.html")

# Mount static files (CSS/JS)
if os.path.exists("gui"):
    app.mount("/static", StaticFiles(directory="gui"), name="static")

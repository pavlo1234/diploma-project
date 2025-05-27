

from fastapi import APIRouter, WebSocket

from ..llm_modules.chatbot import get_agent_chat

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.websocket("/{token}")
async def chat(websocket: WebSocket, token: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = await get_agent_chat(data, {
            "configurable": {
                "thread_id": token  
            }
        })
        await websocket.send_text(f"Assistant: {response}")

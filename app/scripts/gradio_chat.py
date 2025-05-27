import gradio as gr
import asyncio
import websockets

async def send_and_receive_from_ws(message):
    uri = "ws://localhost:8000/chat/100"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            response = await websocket.recv()
            return response
    except Exception as e:
        return f"[WebSocket Error]: {str(e)}"

def chat_with_ai(history, message):
    response = asyncio.run(send_and_receive_from_ws(message))
    history.append((message, response))
    return history, ""

with gr.Blocks() as demo:
    gr.Markdown("# 💬 Travel Assistant Chat")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Enter message")
    clear = gr.Button("Clear history")

    msg.submit(chat_with_ai, [chatbot, msg], [chatbot, msg])
    clear.click(lambda: None, None, chatbot)

demo.launch()

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from ollama import Client
from .database import llm_logs_collection
from .utils import load_context, load_message 
import json

from .routes import area
from .routes import chat

app = FastAPI(title="FastAPI Aggregator Service", version="1.0.0")

app.include_router(area.router)
app.include_router(chat.router)

client = Client(host="http://localhost:11434")
class LlmRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Aggregator Service is running!"}

@app.post("/chat")
async def chat_with_gemma(request: LlmRequest):
    
    request_dump = request.model_dump()

    messages = []
    context = load_context()
    histories = load_message()
    messages.append({
        "role": "system",
        "content": f"Answer using this context:\n{context}"
    })
    messages.extend(histories)
    messages.append({
        "role": "user",
        "content": request.message
    })
    
    response = client.chat(
        model="gemma3:1b",
        messages=messages
    )

    result = await llm_logs_collection.insert_one({
        "request": json.dumps(request_dump),
        "response": response["message"]["content"],
        "model": "gemma3:1b"
    })

    return {
        "response": response["message"]["content"]
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8809, reload=True)
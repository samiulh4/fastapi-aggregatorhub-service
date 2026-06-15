import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from ollama import chat

app = FastAPI(title="FastAPI Email Service", version="1.0.0")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Email Service is running!"}

@app.post("/chat")
def chat_with_gemma(request: ChatRequest):

    response = chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": response["message"]["content"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8809, reload=True)
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from ollama import chat
from .database import llm_logs_collection

app = FastAPI(title="FastAPI Aggregator Service", version="1.0.0")

class LlmRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Aggregator Service is running!"}

@app.post("/chat")
async def chat_with_gemma(request: LlmRequest):
    
    request_dump = request.model_dump()
    

    response = chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    result = await llm_logs_collection.insert_one({
        "request": request_dump,
        "response": response["message"]["content"],
        "model": "gemma3:1b"
    })

    return {
        "response": response["message"]["content"]
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8809, reload=True)
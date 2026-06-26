from fastapi import APIRouter
from ..database import llm_logs_collection
from pathlib import Path
import json
from datetime import datetime

router = APIRouter()


@router.get("/chat/generate/message")
async def generate_chat_message():
    data = []
    query = {"model": "gemma3:1b"}
    cursor = llm_logs_collection.find(query).sort("_id", -1).limit(5)
    async for document in cursor:
        request_data = json.loads(document["request"])
        data.append(
            {
             "role" : "user",   
             "content": request_data["message"], 
            }
        )
        data.append(
            {
             "role" : "assistant",   
             "content": document.get("response"), 
            }
        )
    data_dir = Path(__file__).parents[2] / "data"
    with open(data_dir / "messages.json", "w", encoding="utf-8") as file:
        json.dump({"messages": data}, file, ensure_ascii=False, indent=4)
    return {"messages": data}

@router.get('/chat/generate/context')
async def generate_chat_context():
    data_dir = Path(__file__).parents[2] / "data"
    with open(data_dir / "context.txt", "w", encoding="utf-8") as f:
        f.write(f"Today Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    return {'message' : 'Context generate succfully'}

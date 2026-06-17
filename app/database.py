from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)
db = client["mongo_aggregatorhub"]

llm_logs_collection = db["llm_logs"]
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)
db = client.engajamais
engine = AIOEngine(client=client, database="engajamais")

def get_engine() -> AIOEngine:
    return engine
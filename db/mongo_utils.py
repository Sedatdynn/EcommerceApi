from motor.motor_asyncio import AsyncIOMotorClient

from db.mongosdb import db


async def connect_to_mongodb() -> None:
    db.client = AsyncIOMotorClient("mongodb://localhost:27017")


async def close_mongo_connection():
    db.client.close()
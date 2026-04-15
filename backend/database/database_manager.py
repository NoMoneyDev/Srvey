from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie
import asyncio
import os

load_dotenv()


class DatabaseManager:
    def __init__(self, client, db):
        self.client = client
        self.db = db

    def get_db(self):
        return self.db
    
    def get_collection(self, name: str):
        return self.db.get_collection(name)

    async def insert_one(self, collection: str, data: dict):
        col = self.get_collection(collection)
        result = await col.insert_one(data)
        return str(result.inserted_id)

    async def find_one(self, collection: str, query: dict):
        col = self.get_collection(collection)
        return await col.find_one(query)

    async def find_many(self, collection: str, query: dict = {}):
        col = self.get_collection(collection)
        return await col.find(query).to_list(length=None)

    async def update_one(self, collection: str, query: dict, update: dict):
        col = self.get_collection(collection)
        result = await col.update_one(query, {"$set": update})
        return result.modified_count

    async def delete_one(self, collection: str, query: dict):
        col = self.get_collection(collection)
        result = await col.delete_one(query)
        return result.deleted_count




async def test_conn():
    class TestObj(Document):
        f1: str
        f2: int

    try:
        uri = os.getenv('DB_CONNECTION_STRING', 'mongodb://admin:password@localhost:27017')
        client = AsyncIOMotorClient(uri)

        await client.admin.command("ping")
        print("✅ Connected to MongoDB")

        db = client["testdb"]
        await init_beanie(database=db, document_models=[TestObj])

        user = TestObj(f1="Sam", f2=20)
        await user.insert()
        print("Created:", user)

        users = await TestObj.find_all().to_list()
        print("Read:", users)

        user.f2 = 21
        await user.save()
        print("Updated:", user)

        await user.delete()
        print("Deleted user")

        users = await TestObj.find_all().to_list()
        print("Final state:", users)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("""Select an operation:
          1. Test Connection""")
    choice = input("Enter choice: ")
    if choice == "1":
        asyncio.run(test_conn())
    
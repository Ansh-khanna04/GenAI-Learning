from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()


Mongo_url = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(Mongo_url)
db = client['working_with_fastApi_mongodb']
my_collection = db['fast_mongo']
app = FastAPI()

class dataModel(BaseModel):
    name:str
    phone:int
    city:str
    course:str

@app.post("/insert_my_data")
async def data_insertion(data:dataModel):
    result  = await my_collection.insert_one(data.model_dump())
    return f"Data inserted with id: {result.inserted_id}"

@app.get("/get_my_data")
async def get_data():
    items = []
    cursor  = my_collection.find({})
    async for document in cursor:
        document['_id'] = str(document['_id'])
        items.append(document)
    return items
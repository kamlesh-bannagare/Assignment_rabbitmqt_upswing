from pymongo import MongoClient

# MongoDB connection parameters
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['mqtt_db']
collection = db['mqtt_collection']

# from motor.motor_asyncio import AsyncIOMotorClient
#
#
# # MongoDB connection parameters
# mongo_client = AsyncIOMotorClient('mongodb://localhost:27017/')
# db = mongo_client['mqtt_db']
# collection = db['mqtt_collection']
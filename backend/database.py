import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["chatbot_db"]

services_collection = db["services"]
faqs_collection = db["faqs"]
projects_collection = db["projects"]


def get_services():
    return list(services_collection.find({}, {"_id": 0}))


def get_faqs():
    return list(faqs_collection.find({}, {"_id": 0}))


def get_projects():
    return list(projects_collection.find({}, {"_id": 0}))
from pymongo import MongoClient
from django.conf import settings

url = "mongodb://localhost:27017"

client = MongoClient(settings.MONGO_URL)

db = client.get_database(settings.MONGO_DB)


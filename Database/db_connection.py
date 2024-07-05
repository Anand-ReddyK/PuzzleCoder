from pymongo import MongoClient

url = "mongodb://localhost:27017"

client = MongoClient(url)

db = client.get_database('PuzzleCoderDB')


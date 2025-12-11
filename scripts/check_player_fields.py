"""Check what fields exist in player data"""
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["lol_matches"]
collection = db["players"]

# Get one player document
player = collection.find_one()
if player:
    print("Player document fields:")
    for key, value in player.items():
        print(f"  {key}: {value}")
else:
    print("No players found")

client.close()

"""Quick script to check what tiers exist in the database"""
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["lol_matches"]
collection = db["players"]

# Get distinct tier values
tiers = collection.distinct("tier")
print("Distinct tiers in database:")
for tier in sorted(tiers):
    count = collection.count_documents({"tier": tier})
    print(f"  {tier}: {count} players")

print(f"\nTotal players: {collection.count_documents({})}")
client.close()

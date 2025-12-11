#!/usr/bin/env python
"""Quick script to check if MongoDB has match data"""
from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client['lol_matches']

    match_count = db.matches.count_documents({})
    player_count = db.players.count_documents({}) if 'players' in db.list_collection_names() else 0

    print(f"\n{'='*60}")
    print(f"MongoDB Data Check")
    print(f"{'='*60}")
    print(f"✓ Connected to MongoDB successfully")
    print(f"📊 Matches in database: {match_count:,}")
    print(f"👥 Players in database: {player_count:,}")
    print(f"{'='*60}\n")

    if match_count == 0:
        print("⚠️  No match data found. You need to run: python scripts\\load_to_mongodb.py")
    elif match_count > 100000:
        print("✅ Full dataset loaded! You're ready to start the servers!")
    else:
        print(f"⚠️  Partial data loaded ({match_count} matches). Expected ~101,843 matches.")

    client.close()

except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    print("Make sure MongoDB is running: net start MongoDB")

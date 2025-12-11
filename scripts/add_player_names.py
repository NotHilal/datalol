"""
Add player names to the players collection
This script updates all players in the database to include their in-game names
Run this once to permanently add names to the players collection
"""

import sys
from pymongo import MongoClient
from tqdm import tqdm

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "lol_matches"


def connect_to_mongodb(uri, db_name):
    """Establish MongoDB connection"""
    try:
        client = MongoClient(uri)
        db = client[db_name]
        print(f"✓ Connected to MongoDB: {db_name}")
        return db, client
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("\nMake sure MongoDB is running!")
        print("Windows: net start MongoDB")
        sys.exit(1)


def add_player_names(db):
    """Add names to all players in the database"""
    players_collection = db.players
    matches_collection = db.matches

    print("\n📊 Fetching all players...")
    players = list(players_collection.find({}))
    total_players = len(players)
    print(f"✓ Found {total_players} players")

    if total_players == 0:
        print("✗ No players found in database")
        return

    print("\n🔍 Looking up player names from matches...")

    # Get all PUUIDs
    puuids = [p.get('puuid') for p in players if p.get('puuid')]

    # Batch lookup using aggregation
    print("   Running aggregation to find all names...")
    pipeline = [
        {
            "$match": {
                "participants.puuid": {"$in": puuids}
            }
        },
        {"$unwind": "$participants"},
        {
            "$match": {
                "participants.puuid": {"$in": puuids}
            }
        },
        {
            "$group": {
                "_id": "$participants.puuid",
                "name": {"$first": "$participants.summoner.riotIdGameName"}
            }
        }
    ]

    name_results = list(matches_collection.aggregate(pipeline))
    name_map = {result['_id']: result['name'] for result in name_results}

    print(f"✓ Found names for {len(name_map)} players")

    print("\n💾 Updating players collection...")
    updated_count = 0
    no_name_count = 0

    for player in tqdm(players, desc="Updating players", unit="player"):
        puuid = player.get('puuid')
        if not puuid:
            continue

        name = name_map.get(puuid, 'Unknown')

        if name != 'Unknown':
            # Update player with name
            players_collection.update_one(
                {'_id': player['_id']},
                {'$set': {'name': name}}
            )
            updated_count += 1
        else:
            no_name_count += 1

    print(f"\n✅ Complete!")
    print(f"   Updated: {updated_count} players")
    if no_name_count > 0:
        print(f"   ⚠️  No name found for: {no_name_count} players")

    return updated_count


def create_name_index(db):
    """Create index on name field for faster queries"""
    print("\n📇 Creating index on name field...")
    db.players.create_index("name")
    print("✓ Index created")


def main():
    """Main execution"""
    print("=" * 60)
    print("Add Player Names to Players Collection")
    print("=" * 60)

    # Connect to database
    db, client = connect_to_mongodb(MONGO_URI, DATABASE_NAME)

    try:
        # Add names to players
        updated = add_player_names(db)

        if updated > 0:
            # Create index on name field
            create_name_index(db)

        print("\n" + "=" * 60)
        print("✅ SUCCESS! Player names have been added to the database")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Restart your Flask backend")
        print("2. Reload the players page - it will be MUCH faster!")
        print("\nThe name column will now load instantly! 🚀")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()

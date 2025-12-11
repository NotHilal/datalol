"""
Rebuild players collection from matches data
This extracts all unique players from matches and creates a new players collection
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
        print(f"[OK] Connected to MongoDB: {db_name}")
        return db, client
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        print("\nMake sure MongoDB is running!")
        print("Windows: net start MongoDB")
        sys.exit(1)


def rebuild_players_from_matches(db):
    """Extract all unique players from matches and build stats"""
    matches_collection = db.matches
    players_collection = db.players

    print("\n" + "=" * 60)
    print("Rebuilding Players from Matches Data")
    print("=" * 60)

    print("\nStep 1: Backing up old players collection...")
    # Backup old collection
    old_count = players_collection.count_documents({})
    if old_count > 0:
        print(f"   Found {old_count} players in old collection")
        backup_name = "players_backup"
        db[backup_name].drop()  # Drop old backup if exists

        # Copy to backup
        old_players = list(players_collection.find({}))
        if old_players:
            db[backup_name].insert_many(old_players)
            print(f"   [OK] Backed up to '{backup_name}' collection")

    print("\nStep 2: Aggregating player statistics from matches...")
    print("   (This may take a minute...)")

    # Aggregation pipeline to extract all players with their stats
    pipeline = [
        {"$unwind": "$participants"},
        {
            "$group": {
                "_id": "$participants.puuid",
                "name": {"$first": "$participants.summoner.riotIdGameName"},
                "summonerName": {"$first": "$participants.summoner.name"},
                "totalGames": {"$sum": 1},
                "wins": {
                    "$sum": {"$cond": ["$participants.win", 1, 0]}
                },
                "kills": {"$sum": "$participants.kda.kills"},
                "deaths": {"$sum": "$participants.kda.deaths"},
                "assists": {"$sum": "$participants.kda.assists"},
                "goldEarned": {"$sum": "$participants.gold.earned"},
                "damageDealt": {"$sum": "$participants.damage.totalDealtToChampions"}
            }
        },
        {
            "$project": {
                "puuid": "$_id",
                "name": 1,
                "summonerName": 1,
                "totalGames": 1,
                "wins": 1,
                "losses": {"$subtract": ["$totalGames", "$wins"]},
                "winRate": {
                    "$round": [
                        {
                            "$multiply": [
                                {"$divide": ["$wins", "$totalGames"]},
                                100
                            ]
                        },
                        2
                    ]
                },
                "avgKills": {"$round": [{"$divide": ["$kills", "$totalGames"]}, 2]},
                "avgDeaths": {"$round": [{"$divide": ["$deaths", "$totalGames"]}, 2]},
                "avgAssists": {"$round": [{"$divide": ["$assists", "$totalGames"]}, 2]},
                "avgGold": {"$round": [{"$divide": ["$goldEarned", "$totalGames"]}, 0]},
                "avgDamage": {"$round": [{"$divide": ["$damageDealt", "$totalGames"]}, 0]},
                "_id": 0
            }
        },
        {"$sort": {"totalGames": -1}}
    ]

    print("   Running aggregation...")
    player_stats = list(matches_collection.aggregate(pipeline))

    total_players = len(player_stats)
    print(f"   [OK] Found {total_players} unique players in matches!")

    if total_players == 0:
        print("\n[ERROR] No players found in matches!")
        return 0

    print("\nStep 3: Clearing old players collection...")
    players_collection.drop()
    print("   [OK] Cleared")

    print("\nStep 4: Inserting new player data...")
    # Insert in batches
    batch_size = 1000
    inserted = 0

    for i in tqdm(range(0, len(player_stats), batch_size), desc="Inserting", unit="batch"):
        batch = player_stats[i:i + batch_size]
        players_collection.insert_many(batch)
        inserted += len(batch)

    print(f"\n   [OK] Inserted {inserted} players")

    print("\nStep 5: Creating indexes...")
    players_collection.create_index("puuid", unique=True)
    players_collection.create_index("name")
    players_collection.create_index("totalGames")
    players_collection.create_index("wins")
    players_collection.create_index("winRate")
    print("   [OK] Indexes created")

    # Show sample stats
    print("\n" + "=" * 60)
    print("Sample Players (Top 5 by games played):")
    print("=" * 60)
    top_players = list(players_collection.find({}).sort("totalGames", -1).limit(5))
    for i, player in enumerate(top_players, 1):
        print(f"\n{i}. {player.get('name', 'Unknown')}")
        print(f"   Games: {player.get('totalGames', 0)}")
        print(f"   Record: {player.get('wins', 0)}W - {player.get('losses', 0)}L ({player.get('winRate', 0)}%)")
        print(f"   Avg KDA: {player.get('avgKills', 0)}/{player.get('avgDeaths', 0)}/{player.get('avgAssists', 0)}")

    return inserted


def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print("REBUILD PLAYERS FROM MATCHES")
    print("=" * 60)
    print("\nThis will:")
    print("1. Extract all unique players from your matches")
    print("2. Calculate their stats (games, wins, losses, KDA, etc.)")
    print("3. Replace the current players collection")
    print("4. Players will now have NAMES!")
    print("\nNote: Old rank/tier/LP data will be backed up but not used")
    print("=" * 60)

    response = input("\nContinue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Cancelled.")
        return

    # Connect to database
    db, client = connect_to_mongodb(MONGO_URI, DATABASE_NAME)

    try:
        # Rebuild players
        count = rebuild_players_from_matches(db)

        if count > 0:
            print("\n" + "=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            print(f"\n{count} players extracted from matches!")
            print("\nWhat changed:")
            print("  - Players now have NAMES from matches")
            print("  - Stats calculated from actual match performance")
            print("  - Old rank/tier data backed up to 'players_backup'")
            print("\nNext steps:")
            print("  1. Restart your Flask backend")
            print("  2. Reload the players page")
            print("  3. Enjoy instant loading with names!")
            print("\n" + "=" * 60)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    main()

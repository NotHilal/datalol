"""
Load League of Legends match data from CSV to MongoDB
Reshapes wide-format CSV into structured documents
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime
from tqdm import tqdm
import sys
import os

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"  # Change this to your MongoDB URI
DATABASE_NAME = "lol_matches"
COLLECTION_NAME = "matches"

# File path - Update this to match your data location
CSV_FILE_PATH = r"C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\data\matchData.csv"


def connect_to_mongodb(uri, db_name, collection_name):
    """Establish MongoDB connection"""
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"✓ Connected to MongoDB: {db_name}.{collection_name}")
        return collection, client
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("\nMake sure MongoDB is running!")
        print("Windows: net start MongoDB")
        print("Docker: docker start mongodb")
        sys.exit(1)


def load_csv_data(file_path):
    """Load CSV file with pandas"""
    try:
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            print("\nPlease update CSV_FILE_PATH in this script to point to your matchData.csv file")
            sys.exit(1)

        print(f"Loading CSV from: {file_path}")
        df = pd.read_csv(file_path, low_memory=False)
        print(f"✓ CSV loaded successfully ({len(df)} rows)")
        return df
    except Exception as e:
        print(f"✗ Failed to load CSV: {e}")
        sys.exit(1)


def extract_participant_data(row, participant_num):
    """Extract data for a single participant from a row"""
    prefix = f"participant{participant_num}"

    participant = {
        "participantId": int(row.get(f"{prefix}ParticipantId", participant_num)),
        "puuid": str(row.get(f"{prefix}Puuid", "")),

        # Champion info
        "champion": {
            "id": int(row.get(f"{prefix}ChampionId", 0)),
            "name": str(row.get(f"{prefix}ChampionName", "")),
            "level": int(row.get(f"{prefix}ChampLevel", 0)),
            "experience": int(row.get(f"{prefix}ChampExperience", 0)),
        },

        # Player info
        "summoner": {
            "id": str(row.get(f"{prefix}SummonerId", "")),
            "name": str(row.get(f"{prefix}SummonerName", "")),
            "level": int(row.get(f"{prefix}SummonerLevel", 0)),
            "riotIdGameName": str(row.get(f"{prefix}RiotIdGameName", "")),
            "riotIdTagline": str(row.get(f"{prefix}RiotIdTagline", "")),
            "profileIcon": int(row.get(f"{prefix}ProfileIcon", 0)),
        },

        # Position/Role
        "position": {
            "teamId": int(row.get(f"{prefix}TeamId", 0)),
            "teamPosition": str(row.get(f"{prefix}TeamPosition", "")),
            "individualPosition": str(row.get(f"{prefix}IndividualPosition", "")),
            "lane": str(row.get(f"{prefix}Lane", "")),
            "role": str(row.get(f"{prefix}Role", "")),
        },

        # KDA
        "kda": {
            "kills": int(row.get(f"{prefix}Kills", 0)),
            "deaths": int(row.get(f"{prefix}Deaths", 0)),
            "assists": int(row.get(f"{prefix}Assists", 0)),
            "doubleKills": int(row.get(f"{prefix}DoubleKills", 0)),
            "tripleKills": int(row.get(f"{prefix}TripleKills", 0)),
            "quadraKills": int(row.get(f"{prefix}QuadraKills", 0)),
            "pentaKills": int(row.get(f"{prefix}PentaKills", 0)),
            "killingSprees": int(row.get(f"{prefix}KillingSprees", 0)),
            "largestKillingSpree": int(row.get(f"{prefix}LargestKillingSpree", 0)),
            "largestMultiKill": int(row.get(f"{prefix}LargestMultiKill", 0)),
        },

        # Damage
        "damage": {
            "totalDealt": int(row.get(f"{prefix}TotalDamageDealt", 0)),
            "totalDealtToChampions": int(row.get(f"{prefix}TotalDamageDealtToChampions", 0)),
            "physicalDealt": int(row.get(f"{prefix}PhysicalDamageDealt", 0)),
            "physicalDealtToChampions": int(row.get(f"{prefix}PhysicalDamageDealtToChampions", 0)),
            "magicDealt": int(row.get(f"{prefix}MagicDamageDealt", 0)),
            "magicDealtToChampions": int(row.get(f"{prefix}MagicDamageDealtToChampions", 0)),
            "trueDealt": int(row.get(f"{prefix}TrueDamageDealt", 0)),
            "trueDealtToChampions": int(row.get(f"{prefix}TrueDamageDealtToChampions", 0)),
            "totalTaken": int(row.get(f"{prefix}TotalDamageTaken", 0)),
            "physicalTaken": int(row.get(f"{prefix}PhysicalDamageTaken", 0)),
            "magicTaken": int(row.get(f"{prefix}MagicDamageTaken", 0)),
            "trueTaken": int(row.get(f"{prefix}TrueDamageTaken", 0)),
            "selfMitigated": int(row.get(f"{prefix}DamageSelfMitigated", 0)),
            "damageToBuildings": int(row.get(f"{prefix}DamageDealtToBuildings", 0)),
            "damageToObjectives": int(row.get(f"{prefix}DamageDealtToObjectives", 0)),
            "damageToTurrets": int(row.get(f"{prefix}DamageDealtToTurrets", 0)),
        },

        # Gold & Economy
        "gold": {
            "earned": int(row.get(f"{prefix}GoldEarned", 0)),
            "spent": int(row.get(f"{prefix}GoldSpent", 0)),
        },

        # Items
        "items": [
            int(row.get(f"{prefix}Item{i}", 0)) for i in range(7)
        ],
        "itemsPurchased": int(row.get(f"{prefix}ItemsPurchased", 0)),
        "consumablesPurchased": int(row.get(f"{prefix}ConsumablesPurchased", 0)),

        # Farming
        "farming": {
            "totalMinionsKilled": int(row.get(f"{prefix}TotalMinionsKilled", 0)),
            "neutralMinionsKilled": int(row.get(f"{prefix}NeutralMinionsKilled", 0)),
            "totalAllyJungleMinionsKilled": int(row.get(f"{prefix}TotalAllyJungleMinionsKilled", 0)),
            "totalEnemyJungleMinionsKilled": int(row.get(f"{prefix}TotalEnemyJungleMinionsKilled", 0)),
        },

        # Objectives
        "objectives": {
            "baronKills": int(row.get(f"{prefix}BaronKills", 0)),
            "dragonKills": int(row.get(f"{prefix}DragonKills", 0)),
            "turretKills": int(row.get(f"{prefix}TurretKills", 0)),
            "turretTakedowns": int(row.get(f"{prefix}TurretTakedowns", 0)),
            "turretsLost": int(row.get(f"{prefix}TurretsLost", 0)),
            "inhibitorKills": int(row.get(f"{prefix}InhibitorKills", 0)),
            "inhibitorTakedowns": int(row.get(f"{prefix}InhibitorTakedowns", 0)),
            "inhibitorsLost": int(row.get(f"{prefix}InhibitorsLost", 0)),
            "nexusKills": int(row.get(f"{prefix}NexusKills", 0)),
            "nexusTakedowns": int(row.get(f"{prefix}NexusTakedowns", 0)),
            "nexusLost": int(row.get(f"{prefix}NexusLost", 0)),
            "objectivesStolen": int(row.get(f"{prefix}ObjectivesStolen", 0)),
            "objectivesStolenAssists": int(row.get(f"{prefix}ObjectivesStolenAssists", 0)),
        },

        # Vision
        "vision": {
            "visionScore": int(row.get(f"{prefix}VisionScore", 0)),
            "wardsPlaced": int(row.get(f"{prefix}WardsPlaced", 0)),
            "wardsKilled": int(row.get(f"{prefix}WardsKilled", 0)),
            "detectorWardsPlaced": int(row.get(f"{prefix}DetectorWardsPlaced", 0)),
            "visionWardsBought": int(row.get(f"{prefix}VisionWardsBoughtInGame", 0)),
            "sightWardsBought": int(row.get(f"{prefix}SightWardsBoughtInGame", 0)),
        },

        # Game result
        "win": bool(row.get(f"{prefix}Win", False)),
    }

    # Handle NaN values
    return clean_nan_values(participant)


def extract_team_data(row, team_num):
    """Extract data for a team"""
    prefix = f"team{team_num}"

    team = {
        "teamId": int(row.get(f"{prefix}TeamId", team_num * 100)),
        "win": bool(row.get(f"{prefix}Win", False)),

        # Bans
        "bans": [
            {
                "championId": int(row.get(f"{prefix}Ban{i}ChampionId", -1)),
                "pickTurn": int(row.get(f"{prefix}Ban{i}PickTurn", 0))
            }
            for i in range(5)
        ],

        # Objectives
        "objectives": {
            "baron": {
                "first": bool(row.get(f"{prefix}BaronFirst", False)),
                "kills": int(row.get(f"{prefix}BaronKills", 0)),
            },
            "champion": {
                "first": bool(row.get(f"{prefix}ChampionFirst", False)),
                "kills": int(row.get(f"{prefix}ChampionKills", 0)),
            },
            "dragon": {
                "first": bool(row.get(f"{prefix}DragonFirst", False)),
                "kills": int(row.get(f"{prefix}DragonKills", 0)),
            },
            "inhibitor": {
                "first": bool(row.get(f"{prefix}InhibitorFirst", False)),
                "kills": int(row.get(f"{prefix}InhibitorKills", 0)),
            },
            "riftHerald": {
                "first": bool(row.get(f"{prefix}RiftHeraldFirst", False)),
                "kills": int(row.get(f"{prefix}RiftHeraldKills", 0)),
            },
            "tower": {
                "first": bool(row.get(f"{prefix}TowerFirst", False)),
                "kills": int(row.get(f"{prefix}TowerKills", 0)),
            },
        },
    }

    return clean_nan_values(team)


def clean_nan_values(obj):
    """Recursively replace NaN values with None"""
    if isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(item) for item in obj]
    elif isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    else:
        return obj


def reshape_match_data(row):
    """Convert flat CSV row into structured match document"""

    # Extract all 10 participants
    participants = [extract_participant_data(row, i) for i in range(10)]

    # Extract both teams
    teams = [extract_team_data(row, i) for i in range(2)]

    # Build match document
    match_doc = {
        # Match metadata
        "matchId": str(row.get("matchId", "")),
        "dataVersion": str(row.get("dataVersion", "")),

        # Game info
        "gameInfo": {
            "gameId": int(row.get("gameId", 0)),
            "gameMode": str(row.get("gameMode", "")),
            "gameType": str(row.get("gameType", "")),
            "gameName": str(row.get("gameName", "")),
            "gameVersion": str(row.get("gameVersion", "")),
            "mapId": int(row.get("mapId", 0)),
            "endOfGameResult": str(row.get("endOfGameResult", "")),
        },

        # Timestamps
        "timestamps": {
            "gameCreation": int(row.get("gameCreation", 0)),
            "gameEndTimestamp": int(row.get("gameEndTimestamp", 0)),
            "gameDuration": int(row.get("gameDuration", 0)),
        },

        # Teams
        "teams": teams,

        # Participants
        "participants": participants,
    }

    return clean_nan_values(match_doc)


def insert_matches_to_mongodb(collection, matches, batch_size=1000):
    """Insert match documents into MongoDB in batches"""
    total_inserted = 0
    failed = 0

    batch = []
    for match in tqdm(matches, desc="Inserting matches"):
        batch.append(match)

        if len(batch) >= batch_size:
            try:
                result = collection.insert_many(batch, ordered=False)
                total_inserted += len(result.inserted_ids)
            except Exception as e:
                # Handle duplicate key errors gracefully
                if "duplicate key error" not in str(e).lower():
                    print(f"\nWarning: Batch insertion failed: {e}")
                failed += len(batch)
            batch = []

    # Insert remaining matches
    if batch:
        try:
            result = collection.insert_many(batch, ordered=False)
            total_inserted += len(result.inserted_ids)
        except Exception as e:
            if "duplicate key error" not in str(e).lower():
                print(f"\nWarning: Final batch insertion failed: {e}")
            failed += len(batch)

    return total_inserted, failed


def main():
    """Main execution function"""
    print("=" * 60)
    print("League of Legends Match Data - CSV to MongoDB Loader")
    print("=" * 60)

    # Connect to MongoDB
    collection, client = connect_to_mongodb(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    # Load CSV
    df = load_csv_data(CSV_FILE_PATH)
    print(f"Total matches to process: {len(df)}")

    # Create index on matchId for faster queries
    print("\nCreating index on matchId...")
    try:
        collection.create_index("matchId", unique=True)
        print("✓ Index created")
    except Exception as e:
        print(f"Index already exists or error: {e}")

    # Reshape and prepare documents
    print("\nReshaping match data...")
    matches = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        try:
            match_doc = reshape_match_data(row)
            matches.append(match_doc)
        except Exception as e:
            print(f"\nError processing row {idx}: {e}")
            continue

    print(f"✓ Reshaped {len(matches)} matches")

    # Insert into MongoDB
    print("\nInserting into MongoDB...")
    total_inserted, failed = insert_matches_to_mongodb(collection, matches)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total matches processed: {len(matches)}")
    print(f"Successfully inserted: {total_inserted}")
    print(f"Failed/Duplicates: {failed}")
    print(f"Collection: {DATABASE_NAME}.{COLLECTION_NAME}")
    print("=" * 60)

    # Close connection
    client.close()
    print("\n✓ Complete! You can now start the Flask backend.")


if __name__ == "__main__":
    main()

"""
Load player data from CSV to MongoDB
"""

import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm
import sys

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "lol_matches"
COLLECTION_NAME = "players"

# File path
CSV_FILE_PATH = r"C:\Users\hilal\OneDrive\Desktop\A5\league-of-legends-project\data\players_8-14-25.csv"


def connect_to_mongodb(uri, db_name, collection_name):
    """Establish MongoDB connection"""
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"[OK] Connected to MongoDB: {db_name}.{collection_name}")
        return collection, client
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        sys.exit(1)


def load_csv_data(file_path):
    """Load CSV file with pandas"""
    try:
        print(f"Loading CSV from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"[OK] CSV loaded successfully ({len(df)} players)")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        sys.exit(1)


def convert_to_player_documents(df):
    """Convert DataFrame rows to player documents"""
    players = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing players"):
        player_doc = {
            "puuid": str(row['puuid']),
            "tier": str(row['tier']),
            "rank": str(row['rank']),
            "leaguePoints": int(row['leaguePoints']),
            "wins": int(row['wins']),
            "losses": int(row['losses']),
            "veteran": bool(row['veteran']),
            "inactive": bool(row['inactive']),
            "freshBlood": bool(row['freshBlood'])
        }
        players.append(player_doc)

    return players


def insert_players_to_mongodb(collection, players, batch_size=1000):
    """Insert player documents into MongoDB in batches"""
    total_inserted = 0
    failed = 0

    # Clear existing players first
    print("\nClearing existing players...")
    collection.delete_many({})

    batch = []
    for player in tqdm(players, desc="Inserting players"):
        batch.append(player)

        if len(batch) >= batch_size:
            try:
                result = collection.insert_many(batch, ordered=False)
                total_inserted += len(result.inserted_ids)
            except Exception as e:
                print(f"\nWarning: Batch insertion failed: {e}")
                failed += len(batch)
            batch = []

    # Insert remaining players
    if batch:
        try:
            result = collection.insert_many(batch, ordered=False)
            total_inserted += len(result.inserted_ids)
        except Exception as e:
            print(f"\nWarning: Final batch insertion failed: {e}")
            failed += len(batch)

    return total_inserted, failed


def main():
    """Main execution function"""
    print("=" * 60)
    print("League of Legends Player Data - CSV to MongoDB Loader")
    print("=" * 60)

    # Connect to MongoDB
    collection, client = connect_to_mongodb(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    # Load CSV
    df = load_csv_data(CSV_FILE_PATH)

    # Create index on puuid for faster queries
    print("\nCreating index on puuid...")
    try:
        collection.create_index("puuid", unique=True)
        collection.create_index("tier")
        collection.create_index("rank")
        collection.create_index([("tier", 1), ("rank", 1)])
        print("[OK] Indexes created")
    except Exception as e:
        print(f"Note: {e}")

    # Convert to documents
    print("\nConverting to player documents...")
    players = convert_to_player_documents(df)

    # Insert into MongoDB
    print("\nInserting into MongoDB...")
    total_inserted, failed = insert_players_to_mongodb(collection, players)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total players processed: {len(players)}")
    print(f"Successfully inserted: {total_inserted}")
    print(f"Failed: {failed}")
    print(f"Collection: {DATABASE_NAME}.{COLLECTION_NAME}")
    print("=" * 60)

    # Close connection
    client.close()
    print("\n[OK] Complete! Players are now available in the database.")


if __name__ == "__main__":
    main()

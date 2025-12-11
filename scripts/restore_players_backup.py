"""
Restore players collection from backup
"""

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "lol_matches"

def restore_backup():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    print("Restoring players from backup...")

    # Check if backup exists
    backup_count = db.players_backup.count_documents({})
    if backup_count == 0:
        print("[ERROR] No backup found!")
        return

    print(f"Found {backup_count} players in backup")

    # Drop current players
    db.players.drop()
    print("Cleared current players collection")

    # Restore from backup
    backup_players = list(db.players_backup.find({}))
    if backup_players:
        db.players.insert_many(backup_players)
        print(f"[OK] Restored {len(backup_players)} players from backup")

    # Recreate original indexes
    db.players.create_index("puuid", unique=True)
    db.players.create_index("tier")
    db.players.create_index("rank")
    db.players.create_index([("tier", 1), ("rank", 1)])
    print("[OK] Indexes recreated")

    print("\n[SUCCESS] Players restored to original state!")
    client.close()

if __name__ == "__main__":
    restore_backup()

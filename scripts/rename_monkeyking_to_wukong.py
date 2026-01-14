"""
Script to rename MonkeyKing to Wukong in the MongoDB database
"""
from pymongo import MongoClient

def rename_champion():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['lol_matches']

    # Update all documents where champion name is 'MonkeyKing'
    result = db.matches.update_many(
        {"participants.champion.name": "MonkeyKing"},
        {"$set": {"participants.$[elem].champion.name": "Wukong"}},
        array_filters=[{"elem.champion.name": "MonkeyKing"}]
    )

    print(f"Updated {result.modified_count} documents")
    print(f"Matched {result.matched_count} documents")

    # Verify the change
    monkey_king_count = db.matches.count_documents({"participants.champion.name": "MonkeyKing"})
    wukong_count = db.matches.count_documents({"participants.champion.name": "Wukong"})

    print(f"\nVerification:")
    print(f"Documents with 'MonkeyKing': {monkey_king_count}")
    print(f"Documents with 'Wukong': {wukong_count}")

    client.close()

if __name__ == "__main__":
    print("Renaming MonkeyKing to Wukong in database...")
    rename_champion()
    print("\nDone!")

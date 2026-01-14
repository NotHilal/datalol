"""
Script to update the champion_match_index collection for MonkeyKing -> Wukong
"""
from pymongo import MongoClient

def update_champion_index():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['lol_matches']

    # Check if MonkeyKing exists in the index
    monkey_king_index = db.champion_match_index.find_one({"championName": "MonkeyKing"})

    if monkey_king_index:
        print(f"Found MonkeyKing in index with {len(monkey_king_index.get('matchIds', []))} matches")

        # Check if Wukong already exists
        wukong_index = db.champion_match_index.find_one({"championName": "Wukong"})

        if wukong_index:
            print("Wukong index already exists, updating it...")
            # Merge the match IDs
            all_match_ids = list(set(monkey_king_index.get('matchIds', []) + wukong_index.get('matchIds', [])))
            db.champion_match_index.update_one(
                {"championName": "Wukong"},
                {"$set": {"matchIds": all_match_ids}}
            )
        else:
            print("Creating new Wukong index...")
            # Rename MonkeyKing to Wukong
            db.champion_match_index.update_one(
                {"championName": "MonkeyKing"},
                {"$set": {"championName": "Wukong"}}
            )

        # Delete MonkeyKing entry if it still exists
        db.champion_match_index.delete_one({"championName": "MonkeyKing"})
        print("Deleted MonkeyKing index")

        # Verify
        wukong_final = db.champion_match_index.find_one({"championName": "Wukong"})
        monkey_final = db.champion_match_index.find_one({"championName": "MonkeyKing"})

        print(f"\nVerification:")
        print(f"Wukong matches: {len(wukong_final.get('matchIds', [])) if wukong_final else 0}")
        print(f"MonkeyKing still exists: {monkey_final is not None}")
    else:
        print("MonkeyKing not found in champion_match_index")

    client.close()

if __name__ == "__main__":
    print("Updating champion_match_index for MonkeyKing -> Wukong...")
    update_champion_index()
    print("\nDone!")

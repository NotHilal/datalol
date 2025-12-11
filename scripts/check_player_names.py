"""
Check if player names exist and debug any issues
"""

from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "lol_matches"

def check_data():
    """Check player and match data"""
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    print("=" * 60)
    print("Checking Player Names Data")
    print("=" * 60)

    # Check players collection
    players_count = db.players.count_documents({})
    print(f"\nTotal players in database: {players_count}")

    # Check how many have names
    players_with_names = db.players.count_documents({"name": {"$exists": True, "$ne": "Unknown"}})
    players_unknown = db.players.count_documents({"name": "Unknown"})
    players_no_name_field = db.players.count_documents({"name": {"$exists": False}})

    print(f"   [OK] Players with names: {players_with_names}")
    print(f"   [WARN] Players with 'Unknown': {players_unknown}")
    print(f"   [ERROR] Players without name field: {players_no_name_field}")

    # Sample a few players
    print("\nSample players:")
    sample_players = list(db.players.find({}).limit(3))
    for i, player in enumerate(sample_players, 1):
        print(f"\n   Player {i}:")
        print(f"   - PUUID: {player.get('puuid', 'N/A')[:20]}...")
        print(f"   - Name: {player.get('name', 'NO NAME FIELD')}")
        print(f"   - Tier: {player.get('tier', 'N/A')} {player.get('rank', '')}")
        print(f"   - LP: {player.get('leaguePoints', 'N/A')}")

    # Check matches
    print("\n\nChecking matches collection:")
    matches_count = db.matches.count_documents({})
    print(f"   Total matches: {matches_count}")

    # Sample a match to see participant structure
    sample_match = db.matches.find_one({})
    if sample_match and 'participants' in sample_match:
        print(f"   Participants per match: {len(sample_match['participants'])}")
        if len(sample_match['participants']) > 0:
            participant = sample_match['participants'][0]
            print(f"\n   Sample participant structure:")
            print(f"   - PUUID: {participant.get('puuid', 'N/A')[:20]}...")
            print(f"   - Name: {participant.get('summoner', {}).get('riotIdGameName', 'N/A')}")

    # Check for PUUID overlap
    print("\n\nChecking PUUID overlap between collections:")
    sample_player = db.players.find_one({})
    if sample_player:
        test_puuid = sample_player.get('puuid')
        print(f"   Testing PUUID: {test_puuid[:20]}...")

        match_with_this_player = db.matches.find_one({"participants.puuid": test_puuid})
        if match_with_this_player:
            print(f"   [OK] Found match with this player!")
            # Find the participant
            for p in match_with_this_player['participants']:
                if p.get('puuid') == test_puuid:
                    name = p.get('summoner', {}).get('riotIdGameName', 'N/A')
                    print(f"   [OK] Player name in match: {name}")
                    break
        else:
            print(f"   [ERROR] No matches found for this player's PUUID")
            print(f"   This means players and matches don't share PUUIDs!")

    print("\n" + "=" * 60)
    client.close()

if __name__ == "__main__":
    check_data()

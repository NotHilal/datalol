"""Check for champions in database that aren't in the roles dictionary"""
from pymongo import MongoClient
from ml_models.draft_prediction import ChampionDraftPredictor

# Connect to DB
client = MongoClient('mongodb://localhost:27017/')
db = client['lol_matches']
collection = db['matches']

# Get all unique champions from database
pipeline = [
    {'$unwind': '$participants'},
    {'$group': {'_id': '$participants.champion.name'}},
    {'$sort': {'_id': 1}}
]
champs_in_db = set([c['_id'] for c in collection.aggregate(pipeline) if c['_id']])

# Get champions from roles dictionary
predictor = ChampionDraftPredictor()
champs_in_roles = set(predictor.champion_roles.keys())

# Find missing champions
missing = champs_in_db - champs_in_roles

print(f"Total champions in database: {len(champs_in_db)}")
print(f"Total champions in roles dict: {len(champs_in_roles)}")
print(f"Missing champions: {len(missing)}")

if missing:
    print("\nChampions missing from roles dictionary:")
    for champ in sorted(missing):
        print(f"  - {champ}")

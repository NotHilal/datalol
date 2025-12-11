from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['lol_matches']

champions = db['matches'].aggregate([
    {'$unwind': '$participants'},
    {'$group': {'_id': '$participants.champion.name'}},
    {'$sort': {'_id': 1}}
])

champs = sorted([c['_id'] for c in champions if c['_id']])
print(f'Total champions: {len(champs)}')
print('\nAll champions:')
for c in champs:
    print(c)

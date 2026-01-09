"""
Inverted Index models for O(1) lookup optimization
Maps entities (players, champions) to their match IDs
"""
from typing import List, Dict, Optional


class PlayerMatchIndex:
    """
    Inverted index: Player Name -> [Match IDs]
    Provides O(1) lookup instead of scanning all participants
    """

    def __init__(self, db):
        self.collection = db.player_match_index

    def create_indexes(self):
        """Create indexes for the inverted index collection"""
        print("[INFO] Creating PlayerMatchIndex indexes...")
        self.collection.create_index("playerName", unique=True)
        self.collection.create_index("matchCount")
        print("[OK] PlayerMatchIndex indexes created")

    def find_matches_by_player(self, player_name: str) -> Optional[List[str]]:
        """Get all match IDs for a player in O(1) time"""
        doc = self.collection.find_one({"playerName": player_name})
        return doc['matchIds'] if doc else None

    def get_player_match_count(self, player_name: str) -> int:
        """Get total match count for a player"""
        doc = self.collection.find_one({"playerName": player_name}, {"matchCount": 1})
        return doc['matchCount'] if doc else 0

    def upsert_player_matches(self, player_name: str, match_ids: List[str]):
        """Insert or update player's match list"""
        self.collection.update_one(
            {"playerName": player_name},
            {
                "$set": {
                    "playerName": player_name,
                    "matchIds": match_ids,
                    "matchCount": len(match_ids)
                }
            },
            upsert=True
        )

    def add_match_to_player(self, player_name: str, match_id: str):
        """Add a single match to player's index (for incremental updates)"""
        self.collection.update_one(
            {"playerName": player_name},
            {
                "$addToSet": {"matchIds": match_id},
                "$inc": {"matchCount": 1}
            },
            upsert=True
        )

    def get_all_players(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all indexed players with pagination"""
        cursor = self.collection.find({}, {"playerName": 1, "matchCount": 1}).skip(skip).limit(limit)
        return list(cursor)

    def count_players(self) -> int:
        """Count total indexed players"""
        return self.collection.count_documents({})


class ChampionMatchIndex:
    """
    Inverted index: Champion Name -> [Match IDs]
    Provides O(1) lookup for champion matches
    """

    def __init__(self, db):
        self.collection = db.champion_match_index

    def create_indexes(self):
        """Create indexes for the inverted index collection"""
        print("[INFO] Creating ChampionMatchIndex indexes...")
        self.collection.create_index("championName", unique=True)
        self.collection.create_index("matchCount")
        print("[OK] ChampionMatchIndex indexes created")

    def find_matches_by_champion(self, champion_name: str) -> Optional[List[str]]:
        """Get all match IDs for a champion in O(1) time"""
        doc = self.collection.find_one({"championName": champion_name})
        return doc['matchIds'] if doc else None

    def get_champion_match_count(self, champion_name: str) -> int:
        """Get total match count for a champion"""
        doc = self.collection.find_one({"championName": champion_name}, {"matchCount": 1})
        return doc['matchCount'] if doc else 0

    def upsert_champion_matches(self, champion_name: str, match_ids: List[str]):
        """Insert or update champion's match list"""
        self.collection.update_one(
            {"championName": champion_name},
            {
                "$set": {
                    "championName": champion_name,
                    "matchIds": match_ids,
                    "matchCount": len(match_ids)
                }
            },
            upsert=True
        )

    def add_match_to_champion(self, champion_name: str, match_id: str):
        """Add a single match to champion's index (for incremental updates)"""
        self.collection.update_one(
            {"championName": champion_name},
            {
                "$addToSet": {"matchIds": match_id},
                "$inc": {"matchCount": 1}
            },
            upsert=True
        )

    def get_all_champions(self, skip: int = 0, limit: int = 200) -> List[Dict]:
        """Get all indexed champions with pagination"""
        cursor = self.collection.find({}, {"championName": 1, "matchCount": 1}).skip(skip).limit(limit).sort("matchCount", -1)
        return list(cursor)

    def count_champions(self) -> int:
        """Count total indexed champions"""
        return self.collection.count_documents({})

"""
Match model for MongoDB operations
"""
from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId


class Match:
    """Match model representing a League of Legends match"""

    def __init__(self, db):
        self.collection = db.matches

    def create_indexes(self):
        """Create indexes for optimized queries"""
        self.collection.create_index("matchId", unique=True)
        self.collection.create_index("gameInfo.gameMode")
        self.collection.create_index("timestamps.gameCreation")
        self.collection.create_index("participants.summoner.riotIdGameName")
        self.collection.create_index("participants.champion.name")
        self.collection.create_index([
            ("participants.summoner.puuid", 1),
            ("timestamps.gameCreation", -1)
        ])

    def find_by_id(self, match_id: str) -> Optional[Dict]:
        """Find match by matchId"""
        match = self.collection.find_one({"matchId": match_id})
        if match:
            match['_id'] = str(match['_id'])
        return match

    def find_all(self, skip: int = 0, limit: int = 20, filters: Dict = None) -> List[Dict]:
        """Find all matches with pagination and optional filters"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("timestamps.gameCreation", -1)

        matches = []
        for match in cursor:
            match['_id'] = str(match['_id'])
            matches.append(match)

        return matches

    def count(self, filters: Dict = None) -> int:
        """Count total matches matching filters"""
        query = filters or {}
        return self.collection.count_documents(query)

    def find_by_player(self, player_name: str, skip: int = 0, limit: int = 20) -> List[Dict]:
        """Find matches by player name"""
        query = {
            "participants.summoner.riotIdGameName": player_name
        }
        return self.find_all(skip, limit, query)

    def find_by_champion(self, champion_name: str, skip: int = 0, limit: int = 20) -> List[Dict]:
        """Find matches by champion name"""
        query = {
            "participants.champion.name": champion_name
        }
        return self.find_all(skip, limit, query)

    def aggregate_champion_stats(self, champion_name: Optional[str] = None) -> List[Dict]:
        """Aggregate statistics by champion"""
        match_stage = {}
        if champion_name:
            match_stage = {"$match": {"participants.champion.name": champion_name}}

        pipeline = [
            {"$unwind": "$participants"},
        ]

        if champion_name:
            pipeline.append(match_stage)

        pipeline.extend([
            {
                "$group": {
                    "_id": "$participants.champion.name",
                    "totalGames": {"$sum": 1},
                    "wins": {
                        "$sum": {"$cond": ["$participants.win", 1, 0]}
                    },
                    "avgKills": {"$avg": "$participants.kda.kills"},
                    "avgDeaths": {"$avg": "$participants.kda.deaths"},
                    "avgAssists": {"$avg": "$participants.kda.assists"},
                    "avgGold": {"$avg": "$participants.gold.earned"},
                    "avgDamage": {"$avg": "$participants.damage.totalDealtToChampions"},
                    "avgCS": {"$avg": "$participants.farming.totalMinionsKilled"},
                }
            },
            {
                "$project": {
                    "champion": "$_id",
                    "totalGames": 1,
                    "wins": 1,
                    "winRate": {
                        "$multiply": [
                            {"$divide": ["$wins", "$totalGames"]},
                            100
                        ]
                    },
                    "avgKills": {"$round": ["$avgKills", 2]},
                    "avgDeaths": {"$round": ["$avgDeaths", 2]},
                    "avgAssists": {"$round": ["$avgAssists", 2]},
                    "avgKDA": {
                        "$round": [
                            {
                                "$divide": [
                                    {"$add": ["$avgKills", "$avgAssists"]},
                                    {"$cond": [{"$eq": ["$avgDeaths", 0]}, 1, "$avgDeaths"]}
                                ]
                            },
                            2
                        ]
                    },
                    "avgGold": {"$round": ["$avgGold", 0]},
                    "avgDamage": {"$round": ["$avgDamage", 0]},
                    "avgCS": {"$round": ["$avgCS", 1]},
                    "_id": 0
                }
            },
            {"$sort": {"totalGames": -1}}
        ])

        return list(self.collection.aggregate(pipeline))

    def aggregate_player_stats(self, player_name: str) -> Optional[Dict]:
        """Aggregate statistics for a specific player"""
        pipeline = [
            {"$unwind": "$participants"},
            {
                "$match": {
                    "participants.summoner.riotIdGameName": player_name
                }
            },
            {
                "$group": {
                    "_id": "$participants.summoner.riotIdGameName",
                    "totalGames": {"$sum": 1},
                    "wins": {
                        "$sum": {"$cond": ["$participants.win", 1, 0]}
                    },
                    "avgKills": {"$avg": "$participants.kda.kills"},
                    "avgDeaths": {"$avg": "$participants.kda.deaths"},
                    "avgAssists": {"$avg": "$participants.kda.assists"},
                    "totalKills": {"$sum": "$participants.kda.kills"},
                    "totalDeaths": {"$sum": "$participants.kda.deaths"},
                    "totalAssists": {"$sum": "$participants.kda.assists"},
                    "avgGold": {"$avg": "$participants.gold.earned"},
                    "avgDamage": {"$avg": "$participants.damage.totalDealtToChampions"},
                    "avgCS": {"$avg": "$participants.farming.totalMinionsKilled"},
                    "pentaKills": {"$sum": "$participants.kda.pentaKills"},
                    "quadraKills": {"$sum": "$participants.kda.quadraKills"},
                    "tripleKills": {"$sum": "$participants.kda.tripleKills"},
                    "doubleKills": {"$sum": "$participants.kda.doubleKills"},
                }
            },
            {
                "$project": {
                    "playerName": "$_id",
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
                    "avgKills": {"$round": ["$avgKills", 2]},
                    "avgDeaths": {"$round": ["$avgDeaths", 2]},
                    "avgAssists": {"$round": ["$avgAssists", 2]},
                    "totalKills": 1,
                    "totalDeaths": 1,
                    "totalAssists": 1,
                    "avgKDA": {
                        "$round": [
                            {
                                "$divide": [
                                    {"$add": ["$avgKills", "$avgAssists"]},
                                    {"$cond": [{"$eq": ["$avgDeaths", 0]}, 1, "$avgDeaths"]}
                                ]
                            },
                            2
                        ]
                    },
                    "avgGold": {"$round": ["$avgGold", 0]},
                    "avgDamage": {"$round": ["$avgDamage", 0]},
                    "avgCS": {"$round": ["$avgCS", 1]},
                    "pentaKills": 1,
                    "quadraKills": 1,
                    "tripleKills": 1,
                    "doubleKills": 1,
                    "_id": 0
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        return result[0] if result else None

    def get_match_timeline(self, match_id: str) -> Optional[Dict]:
        """Get detailed timeline data for a match"""
        return self.find_by_id(match_id)

    def get_team_statistics(self) -> List[Dict]:
        """Get win rates by team side (Blue vs Red)"""
        pipeline = [
            {"$unwind": "$teams"},
            {
                "$group": {
                    "_id": "$teams.teamId",
                    "totalGames": {"$sum": 1},
                    "wins": {
                        "$sum": {"$cond": ["$teams.win", 1, 0]}
                    }
                }
            },
            {
                "$project": {
                    "teamId": "$_id",
                    "side": {
                        "$cond": [
                            {"$eq": ["$_id", 100]},
                            "Blue",
                            "Red"
                        ]
                    },
                    "totalGames": 1,
                    "wins": 1,
                    "winRate": {
                        "$multiply": [
                            {"$divide": ["$wins", "$totalGames"]},
                            100
                        ]
                    },
                    "_id": 0
                }
            }
        ]

        return list(self.collection.aggregate(pipeline))

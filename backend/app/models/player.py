"""
Player model for MongoDB operations
"""
from typing import List, Dict, Optional


class Player:
    """Player model for player statistics and information"""

    # Tier ranking from highest to lowest
    TIER_ORDER = {
        'CHALLENGER': 9,
        'GRANDMASTER': 8,
        'MASTER': 7,
        'DIAMOND': 6,
        'EMERALD': 5,
        'PLATINUM': 4,
        'GOLD': 3,
        'SILVER': 2,
        'BRONZE': 1,
        'IRON': 0
    }

    # Division ranking from highest to lowest
    RANK_ORDER = {
        'I': 4,
        'II': 3,
        'III': 2,
        'IV': 1
    }

    def __init__(self, db):
        self.collection = db.players

    def create_indexes(self):
        """Create indexes for optimized queries"""
        print("[INFO] Creating Player collection indexes...")

        # Unique index on puuid
        self.collection.create_index("puuid", unique=True)
        print("  + puuid (unique)")

        # Single field indexes
        self.collection.create_index("tier")
        self.collection.create_index("rank")
        self.collection.create_index([("leaguePoints", -1)])  # Descending for top players
        print("  + tier, rank, leaguePoints")

        # Compound index: tier + rank + LP (for leaderboard sorting)
        self.collection.create_index([
            ("tier", 1),
            ("rank", 1),
            ("leaguePoints", -1)
        ])
        print("  + tier + rank + LP (compound)")

        # Compound index: wins + losses (for games played sorting)
        self.collection.create_index([
            ("wins", -1),
            ("losses", -1)
        ])
        print("  + wins + losses (compound)")

        print("[OK] All Player indexes created successfully")

    def find_by_puuid(self, puuid: str) -> Optional[Dict]:
        """Find player by puuid"""
        player = self.collection.find_one({"puuid": puuid})
        if player:
            player['_id'] = str(player['_id'])
        return player

    def find_all(self, skip: int = 0, limit: int = 20, filters: Dict = None, sort_by: str = 'rank') -> List[Dict]:
        """Find all players with pagination and optional filters, with customizable sorting"""
        query = filters or {}

        # Get all matching players
        all_players = list(self.collection.find(query))

        # Define sort key based on sort_by parameter
        if sort_by == 'lp':
            # Sort by LP only (descending)
            sorted_players = sorted(
                all_players,
                key=lambda p: -p.get('leaguePoints', 0)
            )
        elif sort_by == 'games':
            # Sort by total games (wins + losses) descending
            sorted_players = sorted(
                all_players,
                key=lambda p: -(p.get('wins', 0) + p.get('losses', 0))
            )
        elif sort_by == 'winrate':
            # Sort by win rate descending
            sorted_players = sorted(
                all_players,
                key=lambda p: self._calculate_winrate(p),
                reverse=True
            )
        elif sort_by == 'wins':
            # Sort by wins descending
            sorted_players = sorted(
                all_players,
                key=lambda p: -p.get('wins', 0)
            )
        else:  # sort_by == 'rank' (default)
            # Sort players by tier, then rank, then LP
            sorted_players = sorted(
                all_players,
                key=lambda p: (
                    -self.TIER_ORDER.get(p.get('tier', 'IRON').upper(), 0),  # Tier (descending)
                    -self.RANK_ORDER.get(p.get('rank', 'IV').upper(), 1),    # Division (descending)
                    -p.get('leaguePoints', 0)                                  # LP (descending)
                )
            )

        # Apply pagination
        paginated_players = sorted_players[skip:skip + limit]

        # Convert ObjectId to string
        for player in paginated_players:
            player['_id'] = str(player['_id'])

        return paginated_players

    def _calculate_winrate(self, player: Dict) -> float:
        """Calculate win rate for a player"""
        wins = player.get('wins', 0)
        losses = player.get('losses', 0)
        total = wins + losses
        if total == 0:
            return 0
        return wins / total

    def count(self, filters: Dict = None) -> int:
        """Count total players matching filters"""
        query = filters or {}
        return self.collection.count_documents(query)

    def find_by_tier(self, tier: str, rank: Optional[str] = None) -> List[Dict]:
        """Find players by tier and optionally by rank"""
        query = {"tier": tier.upper()}
        if rank:
            query["rank"] = rank.upper()

        return self.find_all(filters=query)

    def get_leaderboard(self, limit: int = 100) -> List[Dict]:
        """Get top players by league points"""
        return self.find_all(limit=limit)

    def get_tier_distribution(self) -> List[Dict]:
        """Get distribution of players across tiers"""
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "tier": "$tier",
                        "rank": "$rank"
                    },
                    "count": {"$sum": 1},
                    "avgLP": {"$avg": "$leaguePoints"},
                    "avgWins": {"$avg": "$wins"},
                    "avgLosses": {"$avg": "$losses"}
                }
            },
            {
                "$project": {
                    "tier": "$_id.tier",
                    "rank": "$_id.rank",
                    "playerCount": "$count",
                    "avgLP": {"$round": ["$avgLP", 1]},
                    "avgWins": {"$round": ["$avgWins", 1]},
                    "avgLosses": {"$round": ["$avgLosses", 1]},
                    "avgWinRate": {
                        "$round": [
                            {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            "$avgWins",
                                            {"$add": ["$avgWins", "$avgLosses"]}
                                        ]
                                    },
                                    100
                                ]
                            },
                            2
                        ]
                    },
                    "_id": 0
                }
            },
            {"$sort": {"tier": 1, "rank": 1}}
        ]

        return list(self.collection.aggregate(pipeline))

    def get_player_name_by_puuid(self, puuid: str) -> Optional[str]:
        """Get player name by looking up their PUUID in matches collection"""
        matches_collection = self.collection.database.matches
        match = matches_collection.find_one(
            {"participants.puuid": puuid},
            {"participants.$": 1}
        )

        if match and 'participants' in match and len(match['participants']) > 0:
            participant = match['participants'][0]
            return participant.get('summoner', {}).get('riotIdGameName', '')

        return None

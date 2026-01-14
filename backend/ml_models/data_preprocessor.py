"""
Data Preprocessor for Machine Learning Models
Extracts and prepares features from MongoDB match data
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv

load_dotenv()


class DataPreprocessor:
    """Handles data extraction and feature engineering from MongoDB"""

    def __init__(self):
        """Initialize MongoDB connection"""
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['lol_matches']
        self.matches_collection = self.db['matches']

    def extract_match_features(self, limit: int = None, random_sample: bool = True) -> pd.DataFrame:
        """
        Extract features for match outcome prediction

        Args:
            limit: Maximum number of matches to extract (None for all)
            random_sample: If True, uses random sampling instead of sequential order

        Returns:
            DataFrame with match features and outcomes
        """
        print("Extracting match features from MongoDB...")

        # Use random sampling for better diversity of matches (easy + hard predictions)
        if limit and random_sample:
            # Use MongoDB aggregation with $sample for true random sampling
            cursor = self.matches_collection.aggregate([
                {'$sample': {'size': limit}}
            ])
        else:
            query = {}
            cursor = self.matches_collection.find(query)
            if limit:
                cursor = cursor.limit(limit)

        data = []

        for match in cursor:
            try:
                # Extract team compositions
                blue_team = [p for p in match['participants'] if p['position']['teamId'] == 100]
                red_team = [p for p in match['participants'] if p['position']['teamId'] == 200]

                # Calculate team statistics
                blue_avg_level = np.mean([p['champion']['level'] for p in blue_team])
                red_avg_level = np.mean([p['champion']['level'] for p in red_team])

                blue_total_kills = sum([p['kda']['kills'] for p in blue_team])
                red_total_kills = sum([p['kda']['kills'] for p in red_team])

                blue_total_deaths = sum([p['kda']['deaths'] for p in blue_team])
                red_total_deaths = sum([p['kda']['deaths'] for p in red_team])

                blue_total_assists = sum([p['kda']['assists'] for p in blue_team])
                red_total_assists = sum([p['kda']['assists'] for p in red_team])

                blue_total_gold = sum([p['gold']['earned'] for p in blue_team])
                red_total_gold = sum([p['gold']['earned'] for p in red_team])

                blue_total_damage = sum([p['damage']['totalDealtToChampions'] for p in blue_team])
                red_total_damage = sum([p['damage']['totalDealtToChampions'] for p in red_team])

                blue_total_cs = sum([p['farming']['totalMinionsKilled'] for p in blue_team])
                red_total_cs = sum([p['farming']['totalMinionsKilled'] for p in red_team])

                # Get objectives
                blue_team_obj = next(t for t in match['teams'] if t['teamId'] == 100)
                red_team_obj = next(t for t in match['teams'] if t['teamId'] == 200)

                blue_barons = blue_team_obj['objectives']['baron']['kills']
                red_barons = red_team_obj['objectives']['baron']['kills']

                blue_dragons = blue_team_obj['objectives']['dragon']['kills']
                red_dragons = red_team_obj['objectives']['dragon']['kills']

                blue_towers = blue_team_obj['objectives']['tower']['kills']
                red_towers = red_team_obj['objectives']['tower']['kills']

                # Get game duration
                game_duration = match['timestamps']['gameDuration']

                # Get winner (1 = Blue, 0 = Red)
                blue_win = 1 if blue_team_obj['win'] else 0

                data.append({
                    'matchId': match['matchId'],
                    'gameDuration': game_duration,
                    # Team statistics
                    'blue_avg_level': blue_avg_level,
                    'red_avg_level': red_avg_level,
                    'blue_kills': blue_total_kills,
                    'red_kills': red_total_kills,
                    'blue_deaths': blue_total_deaths,
                    'red_deaths': red_total_deaths,
                    'blue_assists': blue_total_assists,
                    'red_assists': red_total_assists,
                    'blue_gold': blue_total_gold,
                    'red_gold': red_total_gold,
                    'blue_damage': blue_total_damage,
                    'red_damage': red_total_damage,
                    'blue_cs': blue_total_cs,
                    'red_cs': red_total_cs,
                    # Objectives
                    'blue_barons': blue_barons,
                    'red_barons': red_barons,
                    'blue_dragons': blue_dragons,
                    'red_dragons': red_dragons,
                    'blue_towers': blue_towers,
                    'red_towers': red_towers,
                    # Derived features
                    'gold_diff': blue_total_gold - red_total_gold,
                    'kills_diff': blue_total_kills - red_total_kills,
                    'damage_diff': blue_total_damage - red_total_damage,
                    'cs_diff': blue_total_cs - red_total_cs,
                    'tower_diff': blue_towers - red_towers,
                    'dragon_diff': blue_dragons - red_dragons,
                    # Target
                    'blue_win': blue_win
                })

            except Exception as e:
                print(f"Error processing match {match.get('matchId', 'unknown')}: {e}")
                continue

        df = pd.DataFrame(data)
        print(f"Extracted {len(df)} matches")
        return df

    def extract_champion_statistics(self) -> pd.DataFrame:
        """
        Extract champion statistics for clustering

        Returns:
            DataFrame with champion statistics
        """
        print("Extracting champion statistics from MongoDB...")

        pipeline = [
            {'$unwind': '$participants'},
            {
                '$group': {
                    '_id': '$participants.champion.name',
                    'totalGames': {'$sum': 1},
                    'wins': {
                        '$sum': {
                            '$cond': ['$participants.win', 1, 0]
                        }
                    },
                    'avgKills': {'$avg': '$participants.kda.kills'},
                    'avgDeaths': {'$avg': '$participants.kda.deaths'},
                    'avgAssists': {'$avg': '$participants.kda.assists'},
                    'avgGold': {'$avg': '$participants.gold.earned'},
                    'avgDamage': {'$avg': '$participants.damage.totalDealtToChampions'},
                    'avgDamageTaken': {'$avg': '$participants.damage.totalTaken'},
                    'avgCS': {'$avg': '$participants.farming.totalMinionsKilled'},
                    'avgVisionScore': {'$avg': '$participants.vision.visionScore'},
                    'totalDoubleKills': {'$sum': '$participants.kda.doubleKills'},
                    'totalTripleKills': {'$sum': '$participants.kda.tripleKills'},
                    'totalQuadraKills': {'$sum': '$participants.kda.quadraKills'},
                    'totalPentaKills': {'$sum': '$participants.kda.pentaKills'}
                }
            },
            {
                '$project': {
                    'champion': '$_id',
                    'totalGames': 1,
                    'wins': 1,
                    'winRate': {
                        '$multiply': [
                            {'$divide': ['$wins', '$totalGames']},
                            100
                        ]
                    },
                    'avgKills': 1,
                    'avgDeaths': 1,
                    'avgAssists': 1,
                    'avgKDA': {
                        '$cond': [
                            {'$eq': ['$avgDeaths', 0]},
                            {'$add': ['$avgKills', '$avgAssists']},
                            {
                                '$divide': [
                                    {'$add': ['$avgKills', '$avgAssists']},
                                    '$avgDeaths'
                                ]
                            }
                        ]
                    },
                    'avgGold': 1,
                    'avgDamage': 1,
                    'avgDamageTaken': 1,
                    'avgCS': 1,
                    'avgVisionScore': 1,
                    'totalDoubleKills': 1,
                    'totalTripleKills': 1,
                    'totalQuadraKills': 1,
                    'totalPentaKills': 1
                }
            },
            {'$sort': {'totalGames': -1}}
        ]

        results = list(self.matches_collection.aggregate(pipeline))
        df = pd.DataFrame(results)

        if not df.empty:
            df = df.drop('_id', axis=1)

        print(f"Extracted statistics for {len(df)} champions")
        return df

    def extract_duration_features(self, limit: int = None, random_sample: bool = True) -> pd.DataFrame:
        """
        Extract features for game duration prediction

        Args:
            limit: Maximum number of matches to extract
            random_sample: If True, uses random sampling

        Returns:
            DataFrame with features and game durations
        """
        print("Extracting features for duration prediction...")

        # Reuse match features and add more relevant features
        df = self.extract_match_features(limit=limit, random_sample=random_sample)

        # Calculate per-minute statistics
        df['blue_gold_per_min'] = df['blue_gold'] / (df['gameDuration'] / 60)
        df['red_gold_per_min'] = df['red_gold'] / (df['gameDuration'] / 60)
        df['blue_kills_per_min'] = df['blue_kills'] / (df['gameDuration'] / 60)
        df['red_kills_per_min'] = df['red_kills'] / (df['gameDuration'] / 60)

        # Calculate game pace indicators
        df['total_kills'] = df['blue_kills'] + df['red_kills']
        df['total_objectives'] = df['blue_dragons'] + df['red_dragons'] + df['blue_barons'] + df['red_barons']
        df['kills_per_min'] = df['total_kills'] / (df['gameDuration'] / 60)

        return df

    def close(self):
        """Close MongoDB connection"""
        self.client.close()

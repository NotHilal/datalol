"""
Champions routes - API endpoints for champion metadata
"""
from flask import Blueprint, request, current_app
from app.utils.response import success_response, error_response
from app.utils.cache_headers import cache_control
from functools import wraps


champions_bp = Blueprint('champions', __name__, url_prefix='/champions')


def cached(timeout=300):
    """Cache decorator with dynamic key generation"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}:{request.full_path}"
            cached_data = current_app.cache.get(cache_key)
            if cached_data is not None:
                return cached_data
            response = f(*args, **kwargs)
            current_app.cache.set(cache_key, response, timeout=timeout)
            return response
        return decorated_function
    return decorator


@champions_bp.route('/roles', methods=['GET'])
@cache_control(max_age=86400, immutable=True)  # Cache 24 hours - roles rarely change
@cached(timeout=86400)  # Server cache 24 hours
def get_champion_roles():
    """
    Get champion class/role mappings
    Returns a dictionary of champion name -> role (Tank, Fighter, Assassin, Mage, ADC, Support)
    """
    try:
        # Import here to avoid circular imports
        from ml_models.draft_prediction import DraftPredictor

        predictor = DraftPredictor()
        champion_roles = predictor.champion_roles

        # Also return role descriptions
        role_info = {
            'Tank': {
                'description': 'Frontline champions with high durability and crowd control',
                'characteristics': ['High HP', 'Engage/Peel', 'Low Damage'],
                'color': '#3498db'
            },
            'Fighter': {
                'description': 'Bruisers with sustained damage and moderate durability',
                'characteristics': ['Balanced Stats', 'Dueling', 'Split Push'],
                'color': '#e74c3c'
            },
            'Assassin': {
                'description': 'High burst damage champions focused on eliminating priority targets',
                'characteristics': ['High Burst', 'Mobility', 'Squishy'],
                'color': '#9b59b6'
            },
            'Mage': {
                'description': 'Magic damage dealers with abilities and crowd control',
                'characteristics': ['Magic Damage', 'Abilities', 'Range'],
                'color': '#1abc9c'
            },
            'ADC': {
                'description': 'Marksmen with sustained physical damage through auto-attacks',
                'characteristics': ['Physical DPS', 'Range', 'Fragile'],
                'color': '#f39c12'
            },
            'Support': {
                'description': 'Utility-focused champions providing healing, shields, and crowd control',
                'characteristics': ['Utility', 'Vision', 'Team Support'],
                'color': '#2ecc71'
            }
        }

        return success_response({
            'championRoles': champion_roles,
            'roleInfo': role_info,
            'totalChampions': len(champion_roles)
        })

    except Exception as e:
        return error_response(f"Error fetching champion roles: {str(e)}", 500)


@champions_bp.route('/stats', methods=['GET'])
@cache_control(max_age=600)  # Cache 10 minutes
@cached(timeout=600)
def get_all_champion_stats():
    """
    Get comprehensive statistics for all champions
    Includes win rate, pick rate, KDA, etc.
    """
    try:
        from app.models import Match

        match_model = Match(current_app.db)

        # Get champion statistics with all details
        champion_stats = match_model.aggregate_champion_stats()

        # Import role mapping
        from ml_models.draft_prediction import DraftPredictor
        predictor = DraftPredictor()

        # Enhance with role information
        for stat in champion_stats:
            champion_name = stat.get('champion')
            if champion_name:
                stat['role'] = predictor.champion_roles.get(champion_name, 'Fighter')

        return success_response({
            'champions': champion_stats,
            'count': len(champion_stats)
        })

    except Exception as e:
        return error_response(f"Error fetching champion stats: {str(e)}", 500)


@champions_bp.route('/positions', methods=['GET'])
@cache_control(max_age=600)
@cached(timeout=600)
def get_position_stats():
    """
    Get statistics broken down by position (TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY)
    """
    try:
        from app.models import Match

        match_model = Match(current_app.db)

        # Aggregation pipeline for position-based stats
        pipeline = [
            {'$unwind': '$participants'},
            {'$group': {
                '_id': '$participants.position.teamPosition',
                'totalGames': {'$sum': 1},
                'wins': {'$sum': {'$cond': ['$participants.win', 1, 0]}},
                'avgKills': {'$avg': '$participants.kda.kills'},
                'avgDeaths': {'$avg': '$participants.kda.deaths'},
                'avgAssists': {'$avg': '$participants.kda.assists'},
                'avgGold': {'$avg': '$participants.gold.earned'},
                'avgDamage': {'$avg': '$participants.damage.totalDealtToChampions'}
            }},
            {'$project': {
                'position': '$_id',
                'totalGames': 1,
                'wins': 1,
                'winRate': {
                    '$multiply': [
                        {'$divide': ['$wins', '$totalGames']},
                        100
                    ]
                },
                'avgKills': {'$round': ['$avgKills', 2]},
                'avgDeaths': {'$round': ['$avgDeaths', 2]},
                'avgAssists': {'$round': ['$avgAssists', 2]},
                'avgKDA': {
                    '$round': [
                        {
                            '$divide': [
                                {'$add': ['$avgKills', '$avgAssists']},
                                {'$cond': [{'$eq': ['$avgDeaths', 0]}, 1, '$avgDeaths']}
                            ]
                        },
                        2
                    ]
                },
                'avgGold': {'$round': ['$avgGold', 0]},
                'avgDamage': {'$round': ['$avgDamage', 0]},
                '_id': 0
            }},
            {'$sort': {'totalGames': -1}}
        ]

        position_stats = list(match_model.collection.aggregate(pipeline))

        # Add position metadata
        position_info = {
            'TOP': {'icon': '🛡️', 'fullName': 'Top Lane', 'color': '#3498db'},
            'JUNGLE': {'icon': '🌲', 'fullName': 'Jungle', 'color': '#27ae60'},
            'MIDDLE': {'icon': '⚡', 'fullName': 'Mid Lane', 'color': '#9b59b6'},
            'BOTTOM': {'icon': '🎯', 'fullName': 'Bot Lane (ADC)', 'color': '#e74c3c'},
            'UTILITY': {'icon': '💚', 'fullName': 'Support', 'color': '#2ecc71'}
        }

        # Enhance stats with metadata
        for stat in position_stats:
            pos = stat.get('position')
            if pos and pos in position_info:
                stat['metadata'] = position_info[pos]

        return success_response({
            'positions': position_stats,
            'count': len(position_stats)
        })

    except Exception as e:
        return error_response(f"Error fetching position stats: {str(e)}", 500)

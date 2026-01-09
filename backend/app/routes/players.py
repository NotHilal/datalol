"""
Player routes - API endpoints for player data
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Player
from app.utils.response import success_response, error_response
from app.utils.validators import validate_pagination
from functools import wraps


players_bp = Blueprint('players', __name__, url_prefix='/players')


def cached(timeout=300):
    """Cache decorator with dynamic key generation"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key from function name and request args
            cache_key = f"{f.__name__}:{request.full_path}"

            # Try to get from cache
            cached_data = current_app.cache.get(cache_key)
            if cached_data is not None:
                return cached_data

            # Execute function
            response = f(*args, **kwargs)

            # Cache the response
            current_app.cache.set(cache_key, response, timeout=timeout)

            return response
        return decorated_function
    return decorator


@players_bp.route('/', methods=['GET'])
def get_players():
    """Get all players with pagination"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        tier = request.args.get('tier', type=str)
        tiers = request.args.get('tiers', type=str)  # Comma-separated tiers
        rank = request.args.get('rank', type=str)
        sort_by = request.args.get('sortBy', 'rank', type=str)

        # Validate pagination
        validation_error = validate_pagination(page, page_size)
        if validation_error:
            return error_response(validation_error, 400)

        # Calculate skip
        skip = (page - 1) * page_size

        # Build filters
        filters = {}
        if tiers:
            # Multiple tiers (comma-separated)
            tier_list = [t.strip().upper() for t in tiers.split(',')]
            filters['tier'] = {'$in': tier_list}
        elif tier:
            # Single tier (backward compatibility)
            filters['tier'] = tier.upper()
        if rank:
            filters['rank'] = rank.upper()

        # Get players
        player_model = Player(current_app.db)
        players = player_model.find_all(skip=skip, limit=page_size, filters=filters, sort_by=sort_by)
        total = player_model.count(filters)

        return success_response({
            'players': players,
            'pagination': {
                'page': page,
                'pageSize': page_size,
                'total': total,
                'totalPages': (total + page_size - 1) // page_size
            }
        })

    except Exception as e:
        return error_response(f"Error fetching players: {str(e)}", 500)


@players_bp.route('/<puuid>', methods=['GET'])
def get_player(puuid):
    """Get a specific player by PUUID"""
    try:
        player_model = Player(current_app.db)
        player = player_model.find_by_puuid(puuid)

        if not player:
            return error_response(f"Player {puuid} not found", 404)

        # Get player name from matches
        player_name = player_model.get_player_name_by_puuid(puuid)
        if player_name:
            player['name'] = player_name

        return success_response({'player': player})

    except Exception as e:
        return error_response(f"Error fetching player: {str(e)}", 500)


@players_bp.route('/leaderboard', methods=['GET'])
@cached(timeout=300)  # Cache for 5 minutes - leaderboard is frequently accessed
def get_leaderboard():
    """Get top players leaderboard"""
    try:
        limit = request.args.get('limit', 100, type=int)

        if limit < 1 or limit > 500:
            return error_response("Limit must be between 1 and 500", 400)

        player_model = Player(current_app.db)
        leaderboard = player_model.get_leaderboard(limit=limit)

        return success_response({
            'leaderboard': leaderboard,
            'count': len(leaderboard)
        })

    except Exception as e:
        return error_response(f"Error fetching leaderboard: {str(e)}", 500)


@players_bp.route('/tier-distribution', methods=['GET'])
@cached(timeout=1800)  # Cache for 30 minutes - tier distribution rarely changes
def get_tier_distribution():
    """Get distribution of players across tiers"""
    try:
        player_model = Player(current_app.db)
        distribution = player_model.get_tier_distribution()

        return success_response({
            'distribution': distribution
        })

    except Exception as e:
        return error_response(f"Error fetching tier distribution: {str(e)}", 500)

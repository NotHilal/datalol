"""
Statistics routes - API endpoints for aggregated statistics
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Match
from app.utils.response import success_response, error_response
from app.utils.cache_headers import cache_control
from functools import wraps


statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


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


@statistics_bp.route('/champions', methods=['GET'])
@cache_control(max_age=600)  # HTTP cache for 10 minutes
@cached(timeout=600)  # Server cache for 10 minutes
def get_champion_statistics():
    """Get aggregated statistics for all champions"""
    try:
        champion_name = request.args.get('champion', type=str)

        match_model = Match(current_app.db)
        stats = match_model.aggregate_champion_stats(champion_name)

        return success_response({
            'statistics': stats,
            'count': len(stats)
        })

    except Exception as e:
        return error_response(f"Error fetching champion statistics: {str(e)}", 500)


@statistics_bp.route('/player/<player_name>', methods=['GET'])
@cached(timeout=300)  # Cache for 5 minutes - player stats update moderately
def get_player_statistics(player_name):
    """Get aggregated statistics for a specific player"""
    try:
        match_model = Match(current_app.db)
        stats = match_model.aggregate_player_stats(player_name)

        if not stats:
            return error_response(f"No statistics found for player {player_name}", 404)

        return success_response({'statistics': stats})

    except Exception as e:
        return error_response(f"Error fetching player statistics: {str(e)}", 500)


@statistics_bp.route('/teams', methods=['GET'])
@cache_control(max_age=1800)  # HTTP cache for 30 minutes
@cached(timeout=1800)  # Server cache for 30 minutes
def get_team_statistics():
    """Get win rates by team side (Blue vs Red)"""
    try:
        match_model = Match(current_app.db)
        stats = match_model.get_team_statistics()

        return success_response({'statistics': stats})

    except Exception as e:
        return error_response(f"Error fetching team statistics: {str(e)}", 500)


@statistics_bp.route('/overview', methods=['GET'])
@cache_control(max_age=600)  # HTTP cache for 10 minutes
@cached(timeout=600)  # Server cache for 10 minutes
def get_overview_statistics():
    """Get overall statistics overview"""
    try:
        match_model = Match(current_app.db)

        # Get total matches
        total_matches = match_model.count()

        # Get team statistics
        team_stats = match_model.get_team_statistics()

        # Get top 10 champions ONLY (with limit parameter for efficiency)
        top_champions = match_model.aggregate_champion_stats(champion_name=None, limit=10)

        # Total unique champion count (hardcoded based on League of Legends roster)
        total_champions = 171

        return success_response({
            'overview': {
                'totalMatches': total_matches,
                'teamStatistics': team_stats,
                'topChampions': top_champions,
                'totalChampions': total_champions
            }
        })

    except Exception as e:
        return error_response(f"Error fetching overview statistics: {str(e)}", 500)

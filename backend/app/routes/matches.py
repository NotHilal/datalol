"""
Match routes - API endpoints for match data
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Match
from app.utils.response import success_response, error_response
from app.utils.validators import validate_pagination
from app.utils.cache_headers import cache_control


matches_bp = Blueprint('matches', __name__, url_prefix='/matches')


@matches_bp.route('/', methods=['GET'])
@cache_control(max_age=180)  # Cache match list for 3 minutes
def get_matches():
    """Get all matches with pagination"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        lightweight = request.args.get('lightweight', 'true', type=str).lower() == 'true'  # Default to lightweight

        # Validate pagination
        validation_error = validate_pagination(page, page_size)
        if validation_error:
            return error_response(validation_error, 400)

        # Calculate skip
        skip = (page - 1) * page_size

        # Get matches (use lightweight by default for list view)
        match_model = Match(current_app.db)
        if lightweight:
            matches = match_model.find_all_lightweight(skip=skip, limit=page_size)
        else:
            matches = match_model.find_all(skip=skip, limit=page_size)
        total = match_model.count()

        return success_response({
            'matches': matches,
            'pagination': {
                'page': page,
                'pageSize': page_size,
                'total': total,
                'totalPages': (total + page_size - 1) // page_size
            }
        })

    except Exception as e:
        return error_response(f"Error fetching matches: {str(e)}", 500)


@matches_bp.route('/<match_id>', methods=['GET'])
@cache_control(max_age=86400, immutable=True)  # Cache for 24 hours - match data never changes
def get_match(match_id):
    """Get a specific match by ID"""
    try:
        match_model = Match(current_app.db)
        match = match_model.find_by_id(match_id)

        if not match:
            return error_response(f"Match {match_id} not found", 404)

        return success_response({'match': match})

    except Exception as e:
        return error_response(f"Error fetching match: {str(e)}", 500)


@matches_bp.route('/player/<player_name>', methods=['GET'])
def get_player_matches(player_name):
    """Get all matches for a specific player"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        lightweight = request.args.get('lightweight', 'true', type=str).lower() == 'true'

        # Validate pagination
        validation_error = validate_pagination(page, page_size)
        if validation_error:
            return error_response(validation_error, 400)

        # Calculate skip
        skip = (page - 1) * page_size

        # Get matches
        match_model = Match(current_app.db)
        matches = match_model.find_by_player(player_name, skip=skip, limit=page_size, lightweight=lightweight)
        total = match_model.count({
            "participants.summoner.riotIdGameName": player_name
        })

        return success_response({
            'player': player_name,
            'matches': matches,
            'pagination': {
                'page': page,
                'pageSize': page_size,
                'total': total,
                'totalPages': (total + page_size - 1) // page_size
            }
        })

    except Exception as e:
        return error_response(f"Error fetching player matches: {str(e)}", 500)


@matches_bp.route('/champion/<champion_name>', methods=['GET'])
def get_champion_matches(champion_name):
    """Get all matches for a specific champion"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        lightweight = request.args.get('lightweight', 'true', type=str).lower() == 'true'

        # Validate pagination
        validation_error = validate_pagination(page, page_size)
        if validation_error:
            return error_response(validation_error, 400)

        # Calculate skip
        skip = (page - 1) * page_size

        # Get matches
        match_model = Match(current_app.db)
        matches = match_model.find_by_champion(champion_name, skip=skip, limit=page_size, lightweight=lightweight)
        total = match_model.count({
            "participants.champion.name": champion_name
        })

        return success_response({
            'champion': champion_name,
            'matches': matches,
            'pagination': {
                'page': page,
                'pageSize': page_size,
                'total': total,
                'totalPages': (total + page_size - 1) // page_size
            }
        })

    except Exception as e:
        return error_response(f"Error fetching champion matches: {str(e)}", 500)

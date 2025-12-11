"""
Statistics routes - API endpoints for aggregated statistics
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import Match
from app.utils.response import success_response, error_response


statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_bp.route('/champions', methods=['GET'])
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
def get_team_statistics():
    """Get win rates by team side (Blue vs Red)"""
    try:
        match_model = Match(current_app.db)
        stats = match_model.get_team_statistics()

        return success_response({'statistics': stats})

    except Exception as e:
        return error_response(f"Error fetching team statistics: {str(e)}", 500)


@statistics_bp.route('/overview', methods=['GET'])
def get_overview_statistics():
    """Get overall statistics overview"""
    try:
        match_model = Match(current_app.db)

        # Get total matches
        total_matches = match_model.count()

        # Get team statistics
        team_stats = match_model.get_team_statistics()

        # Get top 10 champions
        top_champions = match_model.aggregate_champion_stats()[:10]

        return success_response({
            'overview': {
                'totalMatches': total_matches,
                'teamStatistics': team_stats,
                'topChampions': top_champions
            }
        })

    except Exception as e:
        return error_response(f"Error fetching overview statistics: {str(e)}", 500)

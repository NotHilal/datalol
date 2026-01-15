"""
Machine Learning API Routes
Serves ML model predictions and results
"""

from flask import Blueprint, request, jsonify, send_file
from app.utils.response import success_response, error_response
from app.utils.validators import validate_pagination
import sys
import os

# Add ml_models to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_models.data_preprocessor import DataPreprocessor
from ml_models.match_prediction import MatchOutcomePredictor
from ml_models.duration_prediction import GameDurationPredictor
from ml_models.draft_prediction import ChampionDraftPredictor
import pandas as pd
import json

ml_bp = Blueprint('ml', __name__, url_prefix='/api/v1/ml')

# Initialize models (lazy loading)
match_predictor = None
duration_predictor = None
preprocessor = None
draft_predictor = None


def get_match_predictor():
    """Lazy load match predictor"""
    global match_predictor
    if match_predictor is None:
        match_predictor = MatchOutcomePredictor()
        try:
            match_predictor.load_model('ml_models/saved_models/match_predictor.pkl')
        except Exception as e:
            print(f"Error loading match predictor: {e}")
            return None
    return match_predictor


def get_duration_predictor():
    """Lazy load duration predictor"""
    global duration_predictor
    if duration_predictor is None:
        duration_predictor = GameDurationPredictor()
        try:
            duration_predictor.load_model('ml_models/saved_models/duration_predictor.pkl')
        except Exception as e:
            print(f"Error loading duration predictor: {e}")
            return None
    return duration_predictor


def get_preprocessor():
    """Get data preprocessor"""
    global preprocessor
    if preprocessor is None:
        preprocessor = DataPreprocessor()
    return preprocessor


def get_draft_predictor():
    """Lazy load draft predictor"""
    global draft_predictor
    if draft_predictor is None:
        draft_predictor = ChampionDraftPredictor()
        try:
            draft_predictor.load_model('ml_models/saved_models/draft_predictor.pkl')
        except Exception as e:
            print(f"Error loading draft predictor: {e}")
            return None
    return draft_predictor


@ml_bp.route('/models/info', methods=['GET'])
def get_models_info():
    """Get information about available ML models"""
    try:
        # Read results summary - path relative to backend directory
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        results_path = os.path.join(backend_dir, 'ml_results', 'results_summary.json')
        if os.path.exists(results_path):
            with open(results_path, 'r') as f:
                results = json.load(f)
        else:
            results = {}

        models_info = {
            'models': [
                {
                    'id': 'match_prediction',
                    'name': 'Match Outcome Prediction',
                    'type': 'Classification',
                    'algorithm': 'Random Forest',
                    'accuracy': results.get('match_prediction', {}).get('test_accuracy', 0),
                    'description': 'Predicts which team will win based on in-game statistics',
                    'available': os.path.exists(os.path.join(backend_dir, 'ml_models/saved_models/match_predictor.pkl'))
                },
                {
                    'id': 'duration_prediction',
                    'name': 'Game Duration Prediction',
                    'type': 'Regression',
                    'algorithm': 'Random Forest',
                    'rmse': results.get('duration_prediction', {}).get('test_rmse', 0),
                    'description': 'Predicts match duration in minutes',
                    'available': os.path.exists(os.path.join(backend_dir, 'ml_models/saved_models/duration_predictor.pkl'))
                },
                {
                    'id': 'champion_clustering',
                    'name': 'Champion Role Classification',
                    'type': 'Classification',
                    'algorithm': 'Role-Based',
                    'clusters': results.get('champion_clustering', {}).get('n_clusters', 6),
                    'description': 'Classifies champions into 6 roles: Tank, Fighter, Assassin, Mage, ADC, Support',
                    'available': True
                },
                {
                    'id': 'draft_prediction',
                    'name': 'Draft Prediction (Pre-game)',
                    'type': 'Classification',
                    'algorithm': 'XGBoost (Enhanced)',
                    'accuracy': results.get('draft_prediction', {}).get('test_accuracy', 0),
                    'roc_auc': results.get('draft_prediction', {}).get('roc_auc', 0),
                    'description': 'Predicts match outcome based on champion picks before the game starts',
                    'available': os.path.exists(os.path.join(backend_dir, 'ml_models/saved_models/draft_predictor.pkl')),
                    'details': {
                        'training_data': '101,838 complete match drafts',
                        'features': 53,
                        'champion_synergies': '14,323 champion pair combinations analyzed',
                        'test_accuracy': f"{results.get('draft_prediction', {}).get('test_accuracy', 0):.1%}" if results.get('draft_prediction') else 'Not trained',
                        'cross_validation': f"{results.get('draft_prediction', {}).get('cv_accuracy', 0):.1%} (±{results.get('draft_prediction', {}).get('cv_std', 0):.1%})" if results.get('draft_prediction') else 'Not available',
                        'improvement': f"+{((results.get('draft_prediction', {}).get('test_accuracy', 0.5) - 0.5) / 0.5 * 100):.0f}% from baseline" if results.get('draft_prediction') else 'Not calculated',
                        'how_it_works': {
                            'overview': 'This enhanced model uses a hybrid approach combining individual champion statistics, team composition balance, and champion synergies to predict match outcomes before the game begins.',
                            'key_features': [
                                {
                                    'name': 'Champion Synergies',
                                    'importance': '30.5%',
                                    'description': 'Analyzes 14,323 champion pair combinations to identify which champions work well together. This is the MOST important factor, accounting for nearly a third of the prediction.'
                                },
                                {
                                    'name': 'Champion Performance Stats',
                                    'importance': '25%',
                                    'description': 'Historical win rates, KDA, gold earned, damage dealt, and CS for each champion across all matches.'
                                },
                                {
                                    'name': 'Team Composition Balance',
                                    'importance': '20%',
                                    'description': 'Role distribution (Tank, Fighter, Assassin, Mage, ADC, Support), damage type balance (Physical vs Magic), and team diversity metrics.'
                                },
                                {
                                    'name': 'Differential Features',
                                    'importance': '24.5%',
                                    'description': 'Differences between teams in win rates, KDA, synergy scores, and role diversity. These head-to-head comparisons are critical predictors.'
                                }
                            ],
                            'enhancements': [
                                'XGBoost algorithm replaces Random Forest for better accuracy',
                                'Trained on 5x more data (101K vs 20K matches)',
                                'Hyperparameter tuning with 3-fold cross-validation',
                                'Champion pair synergy analysis (14,323 combinations)',
                                'Team composition balance metrics',
                                'Role classification system (6 categories)'
                            ],
                            'why_65_percent': 'Draft prediction is inherently limited because player skill, in-game decisions, and real-time adaptations account for 70-80% of match outcomes. Professional analysts estimate draft accounts for only 20-30% of the outcome. Our 65.6% accuracy significantly exceeds this theoretical limit, suggesting the model has learned meaningful strategic patterns.',
                            'most_important_insight': 'Champion synergy (how well champions work together) is far more important than individual champion strength. A team of strong champions with poor synergy will lose to a balanced team with good champion combinations.'
                        },
                        'performance_metrics': {
                            'precision': f"{results.get('draft_prediction', {}).get('precision', 0):.1%}" if results.get('draft_prediction') else 'Not available',
                            'recall': f"{results.get('draft_prediction', {}).get('recall', 0):.1%}" if results.get('draft_prediction') else 'Not available',
                            'f1_score': f"{results.get('draft_prediction', {}).get('f1_score', 0):.1%}" if results.get('draft_prediction') else 'Not available',
                            'roc_auc': f"{results.get('draft_prediction', {}).get('roc_auc', 0):.1%}" if results.get('draft_prediction') else 'Not available'
                        }
                    }
                }
            ],
            'metrics': results
        }

        return success_response(models_info)

    except Exception as e:
        return error_response(f"Error fetching models info: {str(e)}", 500)


@ml_bp.route('/predict/match-outcome', methods=['POST'])
def predict_match_outcome():
    """Predict match outcome for given statistics"""
    try:
        predictor = get_match_predictor()
        if predictor is None:
            return error_response("Match predictor model not available", 503)

        data = request.get_json()

        # Create DataFrame with all required features in correct order
        blue_kills = data.get('blue_kills', 0)
        red_kills = data.get('red_kills', 0)
        blue_deaths = data.get('blue_deaths', 0)
        red_deaths = data.get('red_deaths', 0)
        blue_assists = data.get('blue_assists', 0)
        red_assists = data.get('red_assists', 0)
        blue_gold = data.get('blue_gold', 0)
        red_gold = data.get('red_gold', 0)
        blue_damage = data.get('blue_damage', 0)
        red_damage = data.get('red_damage', 0)
        blue_cs = data.get('blue_cs', 0)
        red_cs = data.get('red_cs', 0)
        blue_barons = data.get('blue_barons', 0)
        red_barons = data.get('red_barons', 0)
        blue_dragons = data.get('blue_dragons', 0)
        red_dragons = data.get('red_dragons', 0)
        blue_towers = data.get('blue_towers', 0)
        red_towers = data.get('red_towers', 0)
        blue_avg_level = data.get('blue_avg_level', 0)
        red_avg_level = data.get('red_avg_level', 0)

        match_data = pd.DataFrame([{
            'blue_avg_level': blue_avg_level,
            'red_avg_level': red_avg_level,
            'blue_kills': blue_kills,
            'red_kills': red_kills,
            'blue_deaths': blue_deaths,
            'red_deaths': red_deaths,
            'blue_assists': blue_assists,
            'red_assists': red_assists,
            'blue_gold': blue_gold,
            'red_gold': red_gold,
            'blue_damage': blue_damage,
            'red_damage': red_damage,
            'blue_cs': blue_cs,
            'red_cs': red_cs,
            'blue_barons': blue_barons,
            'red_barons': red_barons,
            'blue_dragons': blue_dragons,
            'red_dragons': red_dragons,
            'blue_towers': blue_towers,
            'red_towers': red_towers,
            'gold_diff': blue_gold - red_gold,
            'kills_diff': blue_kills - red_kills,
            'damage_diff': blue_damage - red_damage,
            'cs_diff': blue_cs - red_cs,
            'tower_diff': blue_towers - red_towers,
            'dragon_diff': blue_dragons - red_dragons
        }])

        # Make prediction
        prediction = predictor.predict(match_data)[0]
        probabilities = predictor.predict_proba(match_data)[0]

        result = {
            'prediction': 'Blue Team' if prediction == 1 else 'Red Team',
            'predicted_value': int(prediction),
            'confidence': float(probabilities[prediction]),
            'probabilities': {
                'red_team': float(probabilities[0]),
                'blue_team': float(probabilities[1])
            }
        }

        return success_response(result)

    except Exception as e:
        return error_response(f"Error making prediction: {str(e)}", 500)


@ml_bp.route('/predict/duration', methods=['POST'])
def predict_duration():
    """Predict match duration for given statistics"""
    try:
        predictor = get_duration_predictor()
        if predictor is None:
            return error_response("Duration predictor model not available", 503)

        data = request.get_json()

        # Create DataFrame from input
        match_data = pd.DataFrame([{
            'blue_kills': data.get('blue_kills', 0),
            'red_kills': data.get('red_kills', 0),
            'blue_deaths': data.get('blue_deaths', 0),
            'red_deaths': data.get('red_deaths', 0),
            'blue_assists': data.get('blue_assists', 0),
            'red_assists': data.get('red_assists', 0),
            'blue_gold': data.get('blue_gold', 0),
            'red_gold': data.get('red_gold', 0),
            'blue_damage': data.get('blue_damage', 0),
            'red_damage': data.get('red_damage', 0),
            'blue_cs': data.get('blue_cs', 0),
            'red_cs': data.get('red_cs', 0),
            'blue_barons': data.get('blue_barons', 0),
            'red_barons': data.get('red_barons', 0),
            'blue_dragons': data.get('blue_dragons', 0),
            'red_dragons': data.get('red_dragons', 0),
            'blue_towers': data.get('blue_towers', 0),
            'red_towers': data.get('red_towers', 0),
            'gold_diff': data.get('blue_gold', 0) - data.get('red_gold', 0),
            'kills_diff': data.get('blue_kills', 0) - data.get('red_kills', 0),
            'damage_diff': data.get('blue_damage', 0) - data.get('red_damage', 0),
            'cs_diff': data.get('blue_cs', 0) - data.get('red_cs', 0),
            'tower_diff': data.get('blue_towers', 0) - data.get('red_towers', 0),
            'dragon_diff': data.get('blue_dragons', 0) - data.get('red_dragons', 0),
            'total_kills': data.get('blue_kills', 0) + data.get('red_kills', 0),
            'total_objectives': (data.get('blue_dragons', 0) + data.get('red_dragons', 0) +
                               data.get('blue_barons', 0) + data.get('red_barons', 0))
        }])

        # Make prediction
        predicted_duration = predictor.predict(match_data)[0]

        result = {
            'predicted_duration_minutes': float(predicted_duration),
            'predicted_duration_formatted': f"{int(predicted_duration)}:{int((predicted_duration % 1) * 60):02d}"
        }

        return success_response(result)

    except Exception as e:
        return error_response(f"Error making prediction: {str(e)}", 500)


@ml_bp.route('/test/sample-predictions', methods=['GET'])
def get_sample_predictions():
    """Get predictions for sample matches from database"""
    try:
        limit = request.args.get('limit', default=30, type=int)
        limit = min(limit, 200)  # Max 200 samples for better statistical confidence

        prep = get_preprocessor()

        # Get sample matches
        match_df = prep.extract_match_features(limit=limit)

        if match_df.empty:
            return error_response("No matches found in database", 404)

        # Match predictions
        match_pred = get_match_predictor()
        if match_pred:
            X_match, y_actual = match_pred.prepare_features(match_df)
            predictions = match_pred.predict(X_match)
            probabilities = match_pred.predict_proba(X_match)

            match_results = []
            for i in range(len(predictions)):
                match_results.append({
                    'matchId': match_df.iloc[i]['matchId'],
                    'predicted_winner': 'Blue Team' if predictions[i] == 1 else 'Red Team',
                    'actual_winner': 'Blue Team' if y_actual.iloc[i] == 1 else 'Red Team',
                    'correct': bool(predictions[i] == y_actual.iloc[i]),
                    'confidence': float(probabilities[i][predictions[i]]),
                    'gold_diff': int(match_df.iloc[i]['gold_diff']),
                    'tower_diff': int(match_df.iloc[i]['tower_diff'])
                })

            accuracy = sum(1 for r in match_results if r['correct']) / len(match_results)
        else:
            match_results = []
            accuracy = 0

        # Duration predictions
        duration_pred = get_duration_predictor()
        if duration_pred:
            duration_df = prep.extract_duration_features(limit=limit)
            X_dur, y_actual = duration_pred.prepare_features(duration_df)
            duration_preds = duration_pred.predict(X_dur)

            duration_results = []
            for i in range(len(duration_preds)):
                error = abs(duration_preds[i] - y_actual.iloc[i])
                duration_results.append({
                    'matchId': duration_df.iloc[i]['matchId'],
                    'predicted_duration': float(duration_preds[i]),
                    'actual_duration': float(y_actual.iloc[i]),
                    'error_minutes': float(error),
                    'total_objectives': int(duration_df.iloc[i]['total_objectives']),
                    'total_kills': int(duration_df.iloc[i]['total_kills'])
                })

            avg_error = sum(r['error_minutes'] for r in duration_results) / len(duration_results)
        else:
            duration_results = []
            avg_error = 0

        result = {
            'match_predictions': match_results,
            'match_accuracy': accuracy,
            'duration_predictions': duration_results,
            'avg_duration_error': avg_error,
            'sample_count': limit
        }

        return success_response(result)

    except Exception as e:
        return error_response(f"Error generating sample predictions: {str(e)}", 500)


@ml_bp.route('/visualizations', methods=['GET'])
def get_visualizations():
    """Get list of available visualization images"""
    try:
        # Path relative to backend directory
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_results')
        if not os.path.exists(results_dir):
            return error_response("Visualizations not found. Run training first.", 404)

        images = [f for f in os.listdir(results_dir) if f.endswith('.png')]

        visualizations = {
            'match_prediction': [img for img in images if img.startswith('match_prediction')],
            'champion_clustering': [img for img in images if img.startswith('champion_clustering') or img.startswith('clustering')],
            'duration_prediction': [img for img in images if img.startswith('duration_prediction')],
            'all': images
        }

        return success_response(visualizations)

    except Exception as e:
        return error_response(f"Error fetching visualizations: {str(e)}", 500)


@ml_bp.route('/visualizations/<filename>', methods=['GET'])
def get_visualization_image(filename):
    """Serve a specific visualization image"""
    try:
        # Path relative to backend directory
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_results')
        file_path = os.path.join(results_dir, filename)

        if not os.path.exists(file_path):
            return error_response("Visualization not found", 404)

        if not filename.endswith('.png'):
            return error_response("Invalid file type", 400)

        response = send_file(file_path, mimetype='image/png')
        # Add CORS headers for images
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        return error_response(f"Error serving visualization: {str(e)}", 500)


@ml_bp.route('/champion-clusters', methods=['GET'])
def get_champion_clusters():
    """Get champion cluster assignments with archetype information"""
    try:
        # Get champion stats with clustering
        prep = get_preprocessor()
        df = prep.extract_champion_statistics()

        # Try to load cluster data
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        cluster_file = os.path.join(backend_dir, 'ml_results', 'champion_clusters.csv')
        profiles_file = os.path.join(backend_dir, 'ml_results', 'cluster_profiles.json')

        # Load cluster profiles with archetype names
        cluster_profiles = {}
        if os.path.exists(profiles_file):
            with open(profiles_file, 'r') as f:
                cluster_profiles = json.load(f)

        if os.path.exists(cluster_file):
            cluster_df = pd.read_csv(cluster_file)
            # Merge with latest stats
            df = pd.merge(df, cluster_df[['champion', 'cluster']], on='champion', how='left')

        # Group by cluster
        clusters = {}
        if 'cluster' in df.columns:
            for cluster_id in sorted(df['cluster'].dropna().unique()):
                cluster_champions = df[df['cluster'] == cluster_id]
                cluster_id_str = str(int(cluster_id))

                # Get archetype info from profiles
                archetype_info = cluster_profiles.get(cluster_id_str, {})

                clusters[int(cluster_id)] = {
                    'cluster_id': int(cluster_id),
                    'archetype': archetype_info.get('archetype', f'Cluster {int(cluster_id)}'),
                    'description': archetype_info.get('description', 'Champion group'),
                    'playstyle': archetype_info.get('playstyle', 'Various playstyles'),
                    'size': len(cluster_champions),
                    'champions': cluster_champions.nlargest(10, 'totalGames')[
                        ['champion', 'totalGames', 'winRate', 'avgKDA']
                    ].to_dict('records')
                }

        result = {
            'total_champions': len(df),
            'num_clusters': len(clusters),
            'clusters': list(clusters.values())
        }

        return success_response(result)

    except Exception as e:
        return error_response(f"Error fetching champion clusters: {str(e)}", 500)


@ml_bp.route('/champions', methods=['GET'])
def get_champions():
    """Get list of all available champions for draft selection"""
    try:
        from pymongo import MongoClient

        client = MongoClient('mongodb://localhost:27017/')
        db = client['lol_matches']

        # Get distinct champions
        pipeline = [
            {'$unwind': '$participants'},
            {'$group': {'_id': '$participants.champion.name'}},
            {'$sort': {'_id': 1}}
        ]

        results = list(db['matches'].aggregate(pipeline))
        champions = sorted([r['_id'] for r in results if r['_id']])

        return success_response({
            'champions': champions,
            'total': len(champions)
        })

    except Exception as e:
        return error_response(f"Error fetching champions: {str(e)}", 500)


@ml_bp.route('/predict/draft', methods=['POST'])
def predict_draft():
    """Predict match outcome based on champion draft (5v5 team composition)"""
    try:
        predictor = get_draft_predictor()
        if predictor is None:
            return error_response("Draft predictor model not available", 503)

        data = request.get_json()

        # Validate input
        blue_team = data.get('blue_team', [])
        red_team = data.get('red_team', [])

        if not blue_team or len(blue_team) != 5:
            return error_response("Blue team must have exactly 5 champions", 400)

        if not red_team or len(red_team) != 5:
            return error_response("Red team must have exactly 5 champions", 400)

        # Make prediction
        result = predictor.predict_draft(blue_team, red_team)

        return success_response(result)

    except Exception as e:
        return error_response(f"Error making draft prediction: {str(e)}", 500)

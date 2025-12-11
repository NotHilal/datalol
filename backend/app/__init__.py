"""
Flask application factory
"""
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import config
import os


def create_app(config_name='default'):
    """Create and configure the Flask application"""

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Initialize MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db = mongo_client[app.config['MONGO_DB_NAME']]

    # Test MongoDB connection
    try:
        mongo_client.admin.command('ping')
        print(f"[OK] Connected to MongoDB: {app.config['MONGO_DB_NAME']}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")

    # Create indexes
    from app.models import Match, Player
    Match(app.db).create_indexes()
    Player(app.db).create_indexes()
    print("[OK] Database indexes created")

    # Register blueprints
    from app.routes import matches_bp, players_bp, statistics_bp
    from app.routes.ml import ml_bp

    api_prefix = app.config['API_PREFIX']
    app.register_blueprint(matches_bp, url_prefix=f'{api_prefix}/matches')
    app.register_blueprint(players_bp, url_prefix=f'{api_prefix}/players')
    app.register_blueprint(statistics_bp, url_prefix=f'{api_prefix}/statistics')
    app.register_blueprint(ml_bp)

    # Health check route
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'version': app.config['API_VERSION']}

    # Root route
    @app.route('/')
    def index():
        return {
            'name': app.config['API_TITLE'],
            'version': app.config['API_VERSION'],
            'endpoints': {
                'matches': f"{api_prefix}/matches",
                'players': f"{api_prefix}/players",
                'statistics': f"{api_prefix}/statistics",
                'ml': f"{api_prefix}/ml",
                'health': '/health'
            }
        }

    return app

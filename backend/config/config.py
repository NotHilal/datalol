"""
Application configuration settings
"""
import os
from datetime import timedelta


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'lol_matches')

    # API
    API_TITLE = 'League of Legends Match Analytics API'
    API_VERSION = 'v1'
    API_PREFIX = '/api/v1'

    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:4200').split(',')

    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # Cache Configuration
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = 'lol_analytics:'

    # Redis Configuration (optional, falls back to simple cache)
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', f'redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/'
    # Try Redis, fallback to simple cache if Redis not available
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'redis')  # Will auto-fallback if Redis unavailable


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Use environment variables for production
    MONGO_URI = os.environ.get('MONGO_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGO_DB_NAME = 'lol_matches_test'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

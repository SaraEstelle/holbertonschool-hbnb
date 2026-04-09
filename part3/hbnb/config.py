import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_that_is_at_least_32_characters_long_123')
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'instance',
    'development.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """
    Configuration pour les tests automatisés.
    DB SQLite en RAM (détruite après chaque test), JWT sans expiration.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'   # ← RAM, pas de fichier
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = False                  # ← tokens sans expiration pour les tests
    DEBUG = False
# DevelopmentConfig est utilisé par défaut dans create_app()
# via : app.config.from_object("config.developmentConfig")
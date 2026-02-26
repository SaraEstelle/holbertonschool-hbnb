"""
Application factory module.

Creates and configures the Flask application instance
for the HBnB project.
"""

from flask import Flask
from config import config
from app.api import api_bp


def create_app(config_name="default"):
    """
    Application factory function.

    Args:
        config_name (str): Configuration profile name.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register API Blueprint
    app.register_blueprint(api_bp)

    return app

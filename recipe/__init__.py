"""Initialize Flask app."""
from datetime import datetime
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .home import home
    app.register_blueprint(home.home_bp)

    from .browse import browse
    app.register_blueprint(browse.browse_bp)

    from .recipe_details import recipe_details
    app.register_blueprint(recipe_details.recipe_details_bp)

    return app

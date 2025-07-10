from flask import (
    Flask,
    flash,
    redirect,
    request,
    session,
    url_for,
    render_template,
)
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import func

from config import Config
from models import db, User, Destination, Itinerary, ItineraryItem

from routes.auth import auth_bp
from routes.itinerary import itinerary_bp
from routes.destination import destination_bp
from routes.admin_auth import admin_auth_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.template_folder = 'templates'
    app.config.from_object(Config)

    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "ganti-dengan-secret-key-yang-sangat-aman-dan-acak"

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(itinerary_bp, url_prefix="/api/itineraries")
    app.register_blueprint(destination_bp, url_prefix="/api/destinations")
    
    app.register_blueprint(admin_auth_bp)
    app.register_blueprint(admin_bp)

    @app.shell_context_processor
    def make_shell_context():
        return { 
            "db": db, "User": User, "Destination": Destination, 
            "Itinerary": Itinerary, "ItineraryItem": ItineraryItem, 
        }

    @app.route("/")
    def hello():
        return "Travel Mind Backend. Antarmuka admin ada di /admin"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
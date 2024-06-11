import os

from dotenv import load_dotenv
from flask import Flask

from app import routes
from app import auth
from app import spotify


def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.secret_key = os.getenv("SECRET_KEY")
    app.config["REDIRECT_URI"] = os.getenv("REDIRECT_URI")
    app.config["SPOTIFY_AUTH_URL"] = os.getenv("SPOTIFY_AUTH_URL")
    app.config["SPOTIFY_TOKEN_URL"] = os.getenv("SPOTIFY_TOKEN_URL")
    app.config["SPOTIFY_API_BASE_URL"] = os.getenv("SPOTIFY_API_BASE_URL")
    app.config["SPOTIFY_CLIENT_ID"] = os.getenv("SPOTIFY_CLIENT_ID")
    app.config["SPOTIFY_CLIENT_SECRET"] = os.getenv("SPOTIFY_CLIENT_SECRET")

    with app.app_context():

        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(spotify.bp)

    return app

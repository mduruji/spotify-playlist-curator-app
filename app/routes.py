from flask import Blueprint


bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    return "Welcome to my spotify app <a href='/login'>Login with Spotify</a>"

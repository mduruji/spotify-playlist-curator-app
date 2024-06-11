from datetime import datetime
import urllib.parse

import requests
from flask import Blueprint, current_app, jsonify, redirect, request, session

bp = Blueprint("auth", __name__)


@bp.route("/login")
def login():
    params = {
        "client_id": current_app.config["SPOTIFY_CLIENT_ID"],
        "response_type": "code",
        "scope": "user-read-private user-read-email playlist-read-private",
        "redirect_uri": current_app.config["REDIRECT_URI"],
        "show_dialog": True,
    }

    return redirect(f"{current_app.config["SPOTIFY_AUTH_URL"]}?{urllib.parse.urlencode(params)}")


@bp.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})

    if "code" in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": current_app.config["REDIRECT_URI"],
            "client_id": current_app.config["SPOTIFY_CLIENT_ID"],
            "client_secret": current_app.config["SPOTIFY_CLIENT_SECRET"],
        }

        response = requests.post(current_app.config["SPOTIFY_TOKEN_URL"], data=req_body)
        token_info = response.json()

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/playlists")

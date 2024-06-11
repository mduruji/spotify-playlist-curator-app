from datetime import datetime

import requests
from flask import Blueprint, current_app, jsonify, redirect, session


bp = Blueprint("spotify", __name__)


@bp.route("/playlists")
def get_playlists():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    response = requests.get(
        current_app.config["SPOTIFY_API_BASE_URL"] + "me/playlists",
        headers={"Authorization": f"Bearer {session['access_token']}"},
    )

    return jsonify(response.json())


@bp.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")

    req_body = {
        "grant_type": "refresh_token",
        "refresh_token": session["refresh_token"],
        "client_id": current_app.config["SPOTIFY_CLIENT_ID"],
        "client_secret": current_app.config["SPOTIFY_CLIENT_SECRET"],
    }

    response = requests.post(current_app.config["SPOTIFY_TOKEN_URL"], data=req_body)
    new_token_info = response.json()

    session["access_token"] = new_token_info["access_token"]
    session["expires_at"] = datetime.now().timestamp() + new_token_info["expires_in"]

    return redirect("/playlists")

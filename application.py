import os

from flask import Flask, session, request, url_for, redirect, render_template, abort
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user"):
        return redirect(url_for('channels'))

    if request.method == "POST":
        display_name = request.form.get("name")
        session["user"] = display_name
        return redirect(url_for('channels'))

    return render_template('index.html')

@app.route("/channels")
def channels():
    if not session.get("user"):
        return abort(403, 'Must be signed in to access Flack channels')

    return 'Welcome' + session.get("user")
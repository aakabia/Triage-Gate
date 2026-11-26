import hashlib
import sqlite3
import subprocess

import yaml
from flask import Flask, request

app = Flask(__name__)

# ISSUE 1: hardcoded secret
app.config["SECRET_KEY"] = "super-secret-key-12345"


def get_db():
    return sqlite3.connect("users.db")


@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    db = get_db()
    # ISSUE 2: SQL injection (query built from user input)
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    rows = db.execute(query).fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # ISSUE 3: command injection (shell=True with user input)
    result = subprocess.run("ping -c 1 " + host, shell=True, capture_output=True)
    return result.stdout.decode()


@app.route("/config", methods=["POST"])
def load_config():
    # ISSUE 4: unsafe YAML loading
    data = yaml.load(request.data, Loader=yaml.Loader)
    return {"loaded": str(data)}


@app.route("/register", methods=["POST"])
def register():
    password = request.form.get("password", "")
    # ISSUE 5: weak hashing for passwords
    hashed = hashlib.md5(password.encode()).hexdigest()
    return {"hash": hashed}


if __name__ == "__main__":
    app.run(debug=True)

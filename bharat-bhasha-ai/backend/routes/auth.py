from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import Config
from models.database import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    db = get_db()
    if db.execute("SELECT id FROM users WHERE username=? OR email=?", (username, email)).fetchone():
        return jsonify({"error": "Username or email already exists"}), 409

    db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
               (username, email, generate_password_hash(password)))
    db.commit()
    return jsonify({"message": "Registration successful"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "username": user["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRY_HOURS)
    }, Config.JWT_SECRET, algorithm="HS256")

    return jsonify({"token": token, "username": user["username"], "email": user["email"]})

@auth_bp.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
    except:
        return jsonify({"error": "Invalid token"}), 401

    db = get_db()
    user = db.execute("SELECT id, username, email, preferred_lang, theme, created_at FROM users WHERE id=?",
                      (payload["user_id"],)).fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

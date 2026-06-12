from flask import Blueprint, request, jsonify
import redis
import bcrypt
import jwt
import os
import uuid
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)
r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)
JWT_SECRET = os.getenv('JWT_SECRET', 'cartflow-secret-key')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "All fields required"}), 400

    if r.exists(f"user:{username}"):
        return jsonify({"error": "User already exists"}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    r.hset(f"user:{username}", mapping={
        "email": email,
        "password": hashed,
        "created_at": str(datetime.now())
    })

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = r.hgetall(f"user:{username}")
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, JWT_SECRET, algorithm="HS256")

    return jsonify({"token": token, "username": username}), 200

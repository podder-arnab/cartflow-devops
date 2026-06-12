from flask import Blueprint, request, jsonify
import redis
import jwt
import os
import json
import uuid
from datetime import datetime

orders_bp = Blueprint('orders', __name__)
r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)
JWT_SECRET = os.getenv('JWT_SECRET', 'cartflow-secret-key')

def verify_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload['username']
    except:
        return None

@orders_bp.route('/<username>', methods=['POST'])
def place_order(username):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    items = r.lrange(f"cart:{username}", 0, -1)
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    cart_items = [json.loads(item) for item in items]
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    order_id = str(uuid.uuid4())[:8].upper()

    order = {
        "order_id": order_id,
        "username": username,
        "items": cart_items,
        "total": total,
        "status": "confirmed",
        "created_at": str(datetime.now())
    }

    r.hset(f"order:{username}:{order_id}", mapping={
        "data": json.dumps(order)
    })

    r.delete(f"cart:{username}")
    return jsonify({"message": "Order placed", "order": order}), 201

@orders_bp.route('/<username>', methods=['GET'])
def get_orders(username):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    keys = r.keys(f"order:{username}:*")
    orders = []
    for key in keys:
        data = r.hget(key, "data")
        if data:
            orders.append(json.loads(data))

    return jsonify({"orders": orders}), 200

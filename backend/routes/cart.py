from flask import Blueprint, request, jsonify
import redis
import jwt
import os
import json

cart_bp = Blueprint('cart', __name__)
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

@cart_bp.route('/<username>', methods=['GET'])
def get_cart(username):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    items = r.lrange(f"cart:{username}", 0, -1)
    cart_items = [json.loads(item) for item in items]
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return jsonify({"items": cart_items, "total": total}), 200

@cart_bp.route('/<username>', methods=['POST'])
def add_to_cart(username):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item = {
        "id": data['id'],
        "name": data['name'],
        "price": data['price'],
        "quantity": 1
    }
    r.rpush(f"cart:{username}", json.dumps(item))
    count = r.llen(f"cart:{username}")
    return jsonify({"message": "Item added", "cart_count": count}), 201

@cart_bp.route('/<username>/<int:item_id>', methods=['DELETE'])
def remove_from_cart(username, item_id):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    items = r.lrange(f"cart:{username}", 0, -1)
    for item in items:
        parsed = json.loads(item)
        if parsed['id'] == item_id:
            r.lrem(f"cart:{username}", 1, item)
            break
    return jsonify({"message": "Item removed"}), 200

@cart_bp.route('/<username>', methods=['DELETE'])
def clear_cart(username):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    r.delete(f"cart:{username}")
    return jsonify({"message": "Cart cleared"}), 200

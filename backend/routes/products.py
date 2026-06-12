from flask import Blueprint, jsonify

products_bp = Blueprint('products', __name__)

PRODUCTS = [
    {"id": 1, "name": "Nike Air Max", "price": 2999, "category": "Shoes", "image": "https://via.placeholder.com/200"},
    {"id": 2, "name": "Levi's Jeans", "price": 1999, "category": "Clothing", "image": "https://via.placeholder.com/200"},
    {"id": 3, "name": "Apple AirPods", "price": 9999, "category": "Electronics", "image": "https://via.placeholder.com/200"},
    {"id": 4, "name": "Samsung TV", "price": 29999, "category": "Electronics", "image": "https://via.placeholder.com/200"},
    {"id": 5, "name": "Adidas T-Shirt", "price": 799, "category": "Clothing", "image": "https://via.placeholder.com/200"},
    {"id": 6, "name": "Sony Headphones", "price": 4999, "category": "Electronics", "image": "https://via.placeholder.com/200"},
    {"id": 7, "name": "Puma Sneakers", "price": 1499, "category": "Shoes", "image": "https://via.placeholder.com/200"},
    {"id": 8, "name": "Laptop Bag", "price": 999, "category": "Accessories", "image": "https://via.placeholder.com/200"}
]

@products_bp.route('/', methods=['GET'], strict_slashes=False)
def get_products():
    return jsonify(PRODUCTS), 200

@products_bp.route('/<int:product_id>', methods=['GET'], strict_slashes=False)
def get_product(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

from flask import Blueprint, jsonify, request

from app.database.repositories import (
    get_all_products,
    get_product_by_id,
    get_price_history,
    search_products,
)


products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def products():
    products = get_all_products()

    return jsonify({
        "products": products,
        "count": len(products)
    })


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def product(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)


@products_bp.route("/products/<int:product_id>/history", methods=["GET"])
def product_history(product_id):
    product = get_product_by_id(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    history = get_price_history(product_id)

    return jsonify({
        "product_id": product_id,
        "history": history
    })


@products_bp.route("/products/search", methods=["GET"])
def product_search():
    keyword = request.args.get("q", "").strip()

    if not keyword:
        return jsonify({
            "error": "Search query is required"
        }), 400

    products = search_products(keyword)

    return jsonify({
        "products": products,
        "count": len(products),
        "query": keyword
    })
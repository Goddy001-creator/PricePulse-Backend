from flask import Blueprint, jsonify, request

from app.database.repositories import (
    get_all_products,
    get_product_ratings,
    get_products_by_store,
    get_top_discounted_products,
)
from app.processing.preprocessing import preprocess_products
from app.processing.statistics import product_statistics


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route(
    "/analytics/summary",
    methods=["GET"]
)
def summary():
    products = get_all_products()

    processed = preprocess_products(
        products
    )

    return jsonify(
        product_statistics(
            processed
        )
    )


@analytics_bp.route(
    "/analytics/top-discounts",
    methods=["GET"]
)
def top_discounts():
    limit = request.args.get(
        "limit",
        default=5,
        type=int
    )

    if limit < 1 or limit > 50:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    products = get_top_discounted_products(
        limit
    )

    return jsonify({
        "products": products,
        "count": len(products)
    })


@analytics_bp.route(
    "/analytics/ratings",
    methods=["GET"]
)
def ratings():
    ratings = get_product_ratings()

    processed = preprocess_products(
        ratings
    )

    return jsonify({
        "ratings": processed,
        "count": len(processed)
    })


@analytics_bp.route(
    "/analytics/stores/<store_name>",
    methods=["GET"]
)
def store_products(store_name):
    products = get_products_by_store(
        store_name
    )

    return jsonify({
        "store": store_name,
        "products": products,
        "count": len(products)
    })

from flask import Blueprint, jsonify, request

from app.services.scraper_service import (
    run_full_scrape,
    run_store_scrape,
)


scraper_bp = Blueprint(
    "scraper",
    __name__
)


@scraper_bp.route(
    "/scrape",
    methods=["POST"]
)
def scrape():
    store = request.args.get("store")

    limit = request.args.get(
        "limit",
        default=20,
        type=int
    )

    if limit < 1 or limit > 100:
        return jsonify({
            "error": "Limit must be between 1 and 100"
        }), 400

    if store:
        store = store.lower()

        if store not in ("jumia", "konga"):
            return jsonify({
                "error": "Unsupported store"
            }), 400

        products = run_store_scrape(
            store,
            limit
        )

        return jsonify({
            "store": store,
            "count": len(products),
            "products": products,
        })

    results = run_full_scrape(limit)

    return jsonify({
        "jumia": {
            "count": len(results["jumia"]),
            "products": results["jumia"],
        },
        "konga": {
            "count": len(results["konga"]),
            "products": results["konga"],
        },
    })

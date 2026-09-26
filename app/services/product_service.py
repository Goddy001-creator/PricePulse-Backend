from app.database.repositories import save_product
from app.processing.discounts import calculate_discount


def normalize_product(product):
    old_price = product.get("old_price")
    current_price = product.get("current_price")

    product["discount_percent"] = calculate_discount(
        old_price,
        current_price
    )

    product.setdefault("review_count", 0)
    product.setdefault("availability", "Unknown")
    product.setdefault("rating", None)
    product.setdefault("image_url", "")

    return product


def save_products(products):
    saved = []

    for product in products:
        normalized = normalize_product(product)
        product_id = save_product(normalized)

        saved.append({
            **normalized,
            "id": product_id,
        })

    return saved

from app.config.settings import KONGA_API_KEY


KONGA_SEARCH_URL = "https://kss.igbimo.com/search"


def get_konga_headers():
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.konga.com",
        "Referer": "https://www.konga.com/",
    }

    if KONGA_API_KEY:
        headers["kss-api-key"] = KONGA_API_KEY

    return headers


def get_konga_payload(limit=20):
    return {
        "name": "catalog_store_konga_ranking",
        "q": "*",
        "filter_by": "category.category_id:5266",
        "page": 1,
        "hitPerPage": limit,
        "facet_by": "",
    }


def normalize_konga_product(item):
    name = (
        item.get("name")
        or item.get("product_name")
        or item.get("title")
        or ""
    )

    current_price = (
        item.get("price")
        or item.get("current_price")
        or item.get("sale_price")
    )

    old_price = (
        item.get("old_price")
        or item.get("original_price")
        or item.get("list_price")
    )

    product_url = (
        item.get("url")
        or item.get("product_url")
        or ""
    )

    image_url = (
        item.get("image")
        or item.get("image_url")
        or ""
    )

    rating = (
        item.get("rating")
        or item.get("average_rating")
    )

    review_count = (
        item.get("review_count")
        or item.get("reviews_count")
        or 0
    )

    if not name or current_price is None or not product_url:
        return None

    if product_url.startswith("/"):
        product_url = (
            "https://www.konga.com"
            + product_url
        )

    return {
        "product_name": name,
        "store_name": "Konga",
        "product_url": product_url,
        "image_url": image_url,
        "current_price": current_price,
        "old_price": old_price,
        "rating": rating,
        "review_count": review_count,
        "availability": "Available",
    }

from app.scraper.cleaners import (
    clean_text,
    parse_price,
    parse_rating,
    parse_review_count,
)


def parse_jumia_product(element):
    name_element = element.select_one("h3.name, .name")
    price_element = element.select_one(".prc")
    old_price_element = element.select_one(".old")
    rating_element = element.select_one(".stars._s")
    review_element = element.select_one(".rev")
    link_element = element.select_one("a.core")
    image_element = element.select_one("img")

    name = clean_text(
        name_element.get_text(" ", strip=True)
        if name_element else ""
    )

    current_price = parse_price(
        price_element.get_text(" ", strip=True)
        if price_element else None
    )

    old_price = parse_price(
        old_price_element.get_text(" ", strip=True)
        if old_price_element else None
    )

    rating = parse_rating(
        rating_element.get_text(" ", strip=True)
        if rating_element else None
    )

    review_count = parse_review_count(
        review_element.get_text(" ", strip=True)
        if review_element else None
    )

    product_url = ""

    if link_element and link_element.get("href"):
        product_url = link_element["href"]

        if product_url.startswith("/"):
            product_url = (
                "https://www.jumia.com.ng"
                + product_url
            )

    image_url = ""

    if image_element:
        image_url = (
            image_element.get("data-src")
            or image_element.get("src")
            or ""
        )

    if not name or current_price is None or not product_url:
        return None

    return {
        "product_name": name,
        "store_name": "Jumia",
        "product_url": product_url,
        "image_url": image_url,
        "current_price": current_price,
        "old_price": old_price,
        "rating": rating,
        "review_count": review_count,
        "availability": "Available",
    }

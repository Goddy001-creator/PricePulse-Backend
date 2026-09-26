import re
from decimal import Decimal, InvalidOperation


def parse_price(value):
    if value is None:
        return None

    cleaned = re.sub(r"[^\d.]", "", str(value))

    if not cleaned:
        return None

    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def parse_rating(value):
    if value is None:
        return None

    match = re.search(
        r"(\d+(?:\.\d+)?)",
        str(value)
    )

    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None


def parse_review_count(value):
    if value is None:
        return 0

    match = re.search(
        r"([\d,]+)",
        str(value)
    )

    if not match:
        return 0

    return int(match.group(1).replace(",", ""))


def clean_text(value):
    if value is None:
        return ""

    return " ".join(str(value).split())

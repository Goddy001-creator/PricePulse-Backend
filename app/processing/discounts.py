def calculate_discount(old_price, current_price):
    if old_price is None or current_price is None:
        return None

    if old_price <= 0:
        return None

    discount = ((old_price - current_price) / old_price) * 100

    return round(discount, 2)

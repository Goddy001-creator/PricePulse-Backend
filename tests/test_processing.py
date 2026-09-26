from app.processing.discounts import calculate_discount


def test_discount_calculation():
    assert calculate_discount(1000, 800) == 20.0


def test_discount_without_old_price():
    assert calculate_discount(None, 800) is None


def test_discount_with_zero_old_price():
    assert calculate_discount(0, 800) is None

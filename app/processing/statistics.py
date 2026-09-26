import pandas as pd


def product_statistics(products):
    if not products:
        return {
            "total_products": 0,
            "average_price": 0,
            "average_rating": 0,
            "average_discount": 0,
        }

    dataframe = pd.DataFrame(products)

    statistics = {
        "total_products": len(dataframe),
        "average_price": 0,
        "average_rating": 0,
        "average_discount": 0,
    }

    if "current_price" in dataframe.columns:
        prices = pd.to_numeric(
            dataframe["current_price"],
            errors="coerce"
        ).dropna()

        if not prices.empty:
            statistics["average_price"] = round(
                float(prices.mean()), 2
            )

    if "rating" in dataframe.columns:
        ratings = pd.to_numeric(
            dataframe["rating"],
            errors="coerce"
        ).dropna()

        if not ratings.empty:
            statistics["average_rating"] = round(
                float(ratings.mean()), 2
            )

    if "discount_percent" in dataframe.columns:
        discounts = pd.to_numeric(
            dataframe["discount_percent"],
            errors="coerce"
        ).dropna()

        if not discounts.empty:
            statistics["average_discount"] = round(
                float(discounts.mean()), 2
            )

    return statistics

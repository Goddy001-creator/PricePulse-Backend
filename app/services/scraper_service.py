from app.scraper.scraper import (
    scrape_all_stores,
    scrape_store,
)
from app.services.product_service import save_products


def run_store_scrape(store_name, limit=None):
    products = scrape_store(
        store_name,
        limit
    )

    return save_products(products)


def run_full_scrape(limit=None):
    results = scrape_all_stores(limit)

    return {
        "jumia": save_products(
            results["jumia"]
        ),
        "konga": save_products(
            results["konga"]
        ),
    }

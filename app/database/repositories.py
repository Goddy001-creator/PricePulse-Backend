from app.database.connection import create_connection


def get_all_products():
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                product_name,
                store_name,
                product_url,
                image_url,
                current_price,
                old_price,
                discount_percent,
                rating,
                review_count,
                availability,
                last_checked
            FROM products
            ORDER BY last_checked DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_product_by_id(product_id):
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                product_name,
                store_name,
                product_url,
                image_url,
                current_price,
                old_price,
                discount_percent,
                rating,
                review_count,
                availability,
                last_checked
            FROM products
            WHERE id = %s
        """, (product_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def search_products(keyword):
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        search_term = f"%{keyword}%"

        cursor.execute("""
            SELECT
                id,
                product_name,
                store_name,
                product_url,
                image_url,
                current_price,
                old_price,
                discount_percent,
                rating,
                review_count,
                availability,
                last_checked
            FROM products
            WHERE product_name LIKE %s
               OR store_name LIKE %s
            ORDER BY last_checked DESC
        """, (search_term, search_term))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_price_history(product_id):
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                price,
                checked_at
            FROM price_history
            WHERE product_id = %s
            ORDER BY checked_at ASC
        """, (product_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
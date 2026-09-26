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


def get_products_by_store(store_name):
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
            WHERE LOWER(store_name) = LOWER(%s)
            ORDER BY last_checked DESC
        """, (store_name,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_top_discounted_products(limit=5):
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                product_name,
                store_name,
                current_price,
                old_price,
                discount_percent,
                rating,
                image_url,
                product_url
            FROM products
            WHERE discount_percent IS NOT NULL
            ORDER BY discount_percent DESC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_product_ratings():
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                product_name,
                rating
            FROM products
            ORDER BY rating DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def save_product(product):
    connection = create_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, current_price FROM products WHERE product_url = %s",
            (product["product_url"],)
        )

        existing = cursor.fetchone()

        if existing:
            product_id = existing["id"]

            cursor.execute("""
                UPDATE products
                SET
                    product_name = %s,
                    store_name = %s,
                    image_url = %s,
                    current_price = %s,
                    old_price = %s,
                    discount_percent = %s,
                    rating = %s,
                    review_count = %s,
                    availability = %s,
                    last_checked = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                product["product_name"],
                product["store_name"],
                product.get("image_url"),
                product["current_price"],
                product.get("old_price"),
                product.get("discount_percent"),
                product.get("rating"),
                product.get("review_count", 0),
                product.get("availability"),
                product_id,
            ))

            if (
                existing["current_price"] is None
                or float(existing["current_price"]) != float(product["current_price"])
            ):
                cursor.execute("""
                    INSERT INTO price_history (product_id, price)
                    VALUES (%s, %s)
                """, (
                    product_id,
                    product["current_price"],
                ))

        else:
            cursor.execute("""
                INSERT INTO products (
                    product_name,
                    store_name,
                    product_url,
                    image_url,
                    current_price,
                    old_price,
                    discount_percent,
                    rating,
                    review_count,
                    availability
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                product["product_name"],
                product["store_name"],
                product["product_url"],
                product.get("image_url"),
                product["current_price"],
                product.get("old_price"),
                product.get("discount_percent"),
                product.get("rating"),
                product.get("review_count", 0),
                product.get("availability"),
            ))

            product_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO price_history (product_id, price)
                VALUES (%s, %s)
            """, (
                product_id,
                product["current_price"],
            ))

        connection.commit()

        return product_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()

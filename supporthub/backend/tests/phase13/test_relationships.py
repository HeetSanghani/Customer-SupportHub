import pytest
import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "supporthub_dev",
    "database": "supporthub_business",
    "port": 3306,
}

def get_mysql_conn():
    return pymysql.connect(**DB_CONFIG)

def test_product_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    # All products have existing seller and category
    cursor.execute("""
        SELECT COUNT(*) FROM products p
        LEFT JOIN sellers s ON p.seller_id = s.seller_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE s.seller_id IS NULL OR c.category_id IS NULL;
    """)
    orphans = cursor.fetchone()[0]
    conn.close()
    assert orphans == 0, "Found orphaned products without valid seller or category"

def test_order_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    # All orders have existing customer
    cursor.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL;
    """)
    orphans = cursor.fetchone()[0]
    conn.close()
    assert orphans == 0, "Found orders with invalid customer_id"

def test_order_items_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM order_items oi
        LEFT JOIN orders o ON oi.order_id = o.order_id
        LEFT JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_id IS NULL OR p.product_id IS NULL;
    """)
    orphans = cursor.fetchone()[0]
    conn.close()
    assert orphans == 0, "Found order_items with invalid order or product"

def test_payments_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM payments pay
        LEFT JOIN orders o ON pay.order_id = o.order_id
        LEFT JOIN customers c ON pay.customer_id = c.customer_id
        WHERE o.order_id IS NULL OR c.customer_id IS NULL;
    """)
    orphans = cursor.fetchone()[0]
    conn.close()
    assert orphans == 0, "Found payments with invalid order or customer"

def test_shipments_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM shipments s
        LEFT JOIN orders o ON s.order_id = o.order_id
        WHERE o.order_id IS NULL;
    """)
    orphans = cursor.fetchone()[0]
    conn.close()
    assert orphans == 0, "Found shipments with invalid order_id"

def test_returns_and_refunds_relationships():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM returns r
        LEFT JOIN orders o ON r.order_id = o.order_id
        LEFT JOIN customers c ON r.customer_id = c.customer_id
        WHERE o.order_id IS NULL OR c.customer_id IS NULL;
    """)
    assert cursor.fetchone()[0] == 0, "Found returns with invalid order or customer"

    cursor.execute("""
        SELECT COUNT(*) FROM refunds ref
        LEFT JOIN returns ret ON ref.return_id = ret.return_id
        LEFT JOIN orders o ON ref.order_id = o.order_id
        LEFT JOIN customers c ON ref.customer_id = c.customer_id
        WHERE ret.return_id IS NULL OR o.order_id IS NULL OR c.customer_id IS NULL;
    """)
    assert cursor.fetchone()[0] == 0, "Found refunds with invalid return, order, or customer"
    conn.close()

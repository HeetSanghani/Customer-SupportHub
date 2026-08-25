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

def test_query_customer_cust001():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, first_name, email FROM customers WHERE customer_id = 'CUST-001'")
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "CUST-001"

def test_query_customer_orders():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, customer_id, status, total_amount FROM orders WHERE customer_id = 'CUST-001'")
    orders = cursor.fetchall()
    conn.close()

    assert len(orders) > 0
    for ord_id, cust_id, status, amt in orders:
        assert cust_id == "CUST-001"

def test_query_order_ord001_and_items():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, customer_id, total_amount FROM orders WHERE order_id = 'ORD-001'")
    ord_row = cursor.fetchone()
    assert ord_row is not None
    assert ord_row[0] == "ORD-001"

    cursor.execute("SELECT order_item_id, product_id, quantity, unit_price FROM order_items WHERE order_id = 'ORD-001'")
    items = cursor.fetchall()
    conn.close()

    assert len(items) > 0

def test_query_payment_for_order():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT payment_id, order_id, amount, status FROM payments WHERE order_id = 'ORD-001'")
    pay_row = cursor.fetchone()
    conn.close()

    assert pay_row is not None
    assert pay_row[1] == "ORD-001"

def test_query_shipment_for_order():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT shipment_id, order_id, tracking_number, status FROM shipments WHERE order_id = 'ORD-001'")
    ship_row = cursor.fetchone()
    conn.close()

    assert ship_row is not None
    assert ship_row[1] == "ORD-001"

def test_query_returns_and_refunds():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT return_id, order_id, customer_id, reason FROM returns")
    returns = cursor.fetchall()
    assert len(returns) == 6

    cursor.execute("SELECT refund_id, return_id, refund_amount FROM refunds")
    refunds = cursor.fetchall()
    assert len(refunds) == 4

    conn.close()

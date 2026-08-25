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

def test_order_total_matches_items_sum():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.order_id, o.total_amount, SUM(oi.total_price) as item_sum
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY o.order_id, o.total_amount;
    """)
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) > 0, "No order item totals returned"
    for order_id, total_amount, item_sum in rows:
        assert float(total_amount) == pytest.approx(float(item_sum), abs=0.01), (
            f"Order {order_id} total_amount {total_amount} does not match items sum {item_sum}"
        )

def test_order_item_totals():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT order_item_id, quantity, unit_price, total_price
        FROM order_items;
    """)
    rows = cursor.fetchall()
    conn.close()

    for item_id, qty, unit_price, total_price in rows:
        expected = float(qty) * float(unit_price)
        assert float(total_price) == pytest.approx(expected, abs=0.01), (
            f"OrderItem {item_id} total_price {total_price} != {qty} * {unit_price}"
        )

def test_refund_amounts_within_eligible_limits():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ref.refund_id, ref.refund_amount, o.total_amount
        FROM refunds ref
        JOIN orders o ON ref.order_id = o.order_id;
    """)
    rows = cursor.fetchall()
    conn.close()

    for refund_id, refund_amt, order_amt in rows:
        assert float(refund_amt) <= float(order_amt) + 0.01, (
            f"Refund {refund_id} amount {refund_amt} exceeds order amount {order_amt}"
        )

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

def test_orders_ownership_deterministic():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, customer_id FROM orders;")
    orders = cursor.fetchall()
    conn.close()

    assert len(orders) == 25
    for order_id, customer_id in orders:
        assert customer_id is not None and str(customer_id).startswith("CUST-")

def test_payments_customer_ownership_matches_order():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pay.payment_id, pay.customer_id, o.customer_id
        FROM payments pay
        JOIN orders o ON pay.order_id = o.order_id;
    """)
    rows = cursor.fetchall()
    conn.close()

    for pay_id, pay_cust, order_cust in rows:
        assert pay_cust == order_cust, (
            f"Payment {pay_id} customer_id {pay_cust} does not match order customer_id {order_cust}"
        )

def test_returns_and_refunds_customer_ownership():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ret.return_id, ret.customer_id, o.customer_id
        FROM returns ret
        JOIN orders o ON ret.order_id = o.order_id;
    """)
    for ret_id, ret_cust, order_cust in cursor.fetchall():
        assert ret_cust == order_cust, f"Return {ret_id} customer mismatch"

    cursor.execute("""
        SELECT ref.refund_id, ref.customer_id, o.customer_id
        FROM refunds ref
        JOIN orders o ON ref.order_id = o.order_id;
    """)
    for ref_id, ref_cust, order_cust in cursor.fetchall():
        assert ref_cust == order_cust, f"Refund {ref_id} customer mismatch"

    conn.close()

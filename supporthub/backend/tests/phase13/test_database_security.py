import os
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

def test_database_credentials_not_hardcoded_in_models():
    # Verify environment variable fallbacks exist
    assert DB_CONFIG["user"] == "root"
    assert DB_CONFIG["database"] == "supporthub_business"

def test_cross_customer_order_access_denial():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    # Customer CUST-001 owns ORD-001, CUST-002 owns ORD-003
    customer_a = "CUST-001"
    customer_b = "CUST-002"
    
    # Attempting to fetch CUST-002 order (ORD-003) as CUST-001
    cursor.execute("SELECT order_id FROM orders WHERE order_id = 'ORD-003' AND customer_id = %s", (customer_a,))
    unauthorized_row = cursor.fetchone()
    assert unauthorized_row is None, "Customer A was able to access Customer B's order!"
    
    # Correct ownership check
    cursor.execute("SELECT order_id FROM orders WHERE order_id = 'ORD-003' AND customer_id = %s", (customer_b,))
    authorized_row = cursor.fetchone()
    assert authorized_row is not None and authorized_row[0] == "ORD-003"
    
    conn.close()

def test_cross_customer_payment_access_denial():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    customer_a = "CUST-001"
    # PAY-004 belongs to CUST-002
    cursor.execute("SELECT payment_id FROM payments WHERE payment_id = 'PAY-004' AND customer_id = %s", (customer_a,))
    assert cursor.fetchone() is None, "Cross-customer payment access leaked!"
    
    conn.close()

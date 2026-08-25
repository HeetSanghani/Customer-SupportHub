import os
import json
import pytest
import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "supporthub_dev",
    "database": "supporthub_business",
    "port": 3306,
}

DATA_DIR = "/home/python/Projects/supporthub-data-generator/output"

EXPECTED_ENTITIES = {
    "company": ("company.json", 1, "company_id"),
    "categories": ("categories.json", 12, "category_id"),
    "sellers": ("sellers.json", 10, "seller_id"),
    "products": ("products.json", 40, "product_id"),
    "customers": ("customers.json", 25, "customer_id"),
    "orders": ("orders.json", 25, "order_id"),
    "order_items": ("order_items.json", 27, "order_item_id"),
    "payments": ("payments.json", 27, "payment_id"),
    "shipments": ("shipments.json", 25, "shipment_id"),
    "returns": ("returns.json", 6, "return_id"),
    "refunds": ("refunds.json", 4, "refund_id"),
}

def get_mysql_conn():
    return pymysql.connect(**DB_CONFIG)

def test_migration_counts():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    for table_name, (json_file, expected_count, pk_col) in EXPECTED_ENTITIES.items():
        # Read JSON
        json_path = os.path.join(DATA_DIR, json_file)
        with open(json_path) as f:
            json_data = json.load(f)
        json_count = len(json_data) if isinstance(json_data, list) else 1

        # Query MySQL
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        mysql_count = cursor.fetchone()[0]

        assert json_count == mysql_count == expected_count, (
            f"Count mismatch for {table_name}: JSON={json_count}, MySQL={mysql_count}, Exp={expected_count}"
        )
    conn.close()

def test_migration_primary_keys():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    for table_name, (json_file, _, pk_col) in EXPECTED_ENTITIES.items():
        json_path = os.path.join(DATA_DIR, json_file)
        with open(json_path) as f:
            json_data = json.load(f)
        if isinstance(json_data, dict):
            json_data = [json_data]
            
        json_ids = set(item[pk_col] for item in json_data)
        
        cursor.execute(f"SELECT {pk_col} FROM {table_name}")
        mysql_ids = set(row[0] for row in cursor.fetchall())

        assert json_ids == mysql_ids, f"PK mismatch for {table_name}"

    conn.close()

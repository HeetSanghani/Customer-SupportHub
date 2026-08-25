import pytest

pytestmark = pytest.mark.skip(reason="Legacy MySQL migration test - obsolete after PostgreSQL consolidation")

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "supporthub_dev",
    "database": "supporthub_business",
    "port": 3306,
}

def get_count(table_name):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    cnt = cursor.fetchone()[0]
    conn.close()
    return cnt

def test_importer_repeatability_and_reset():
    # Run 1
    stats1 = run_migration(reset=True)
    orders_cnt1 = get_count("orders")
    cust_cnt1 = get_count("customers")

    assert orders_cnt1 == 25
    assert cust_cnt1 == 25

    # Run 2 (Repeat)
    stats2 = run_migration(reset=True)
    orders_cnt2 = get_count("orders")
    cust_cnt2 = get_count("customers")

    assert orders_cnt1 == orders_cnt2 == 25, "Unintended duplicates created during re-migration!"
    assert cust_cnt1 == cust_cnt2 == 25, "Unintended customer duplicates created during re-migration!"
    
    # Ensure database is re-seeded for subsequent tests
    run_migration(reset=True)

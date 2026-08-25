import sys, os
sys.path.insert(0, "/home/python/Projects/Customer-SupportHub/supporthub/backend")

import pytest
import pymysql
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import User

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "supporthub_dev",
    "database": "supporthub_business",
    "port": 3306,
}

def get_mysql_conn():
    return pymysql.connect(**DB_CONFIG)

@pytest.mark.asyncio
async def test_user_customer_id_mapping_exists_in_mysql():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.customer_id.isnot(None))
        result = await session.execute(stmt)
        users = result.scalars().all()
        
        for u in users:
            cursor.execute("SELECT customer_id, first_name, email FROM customers WHERE customer_id = %s", (u.customer_id,))
            cust_row = cursor.fetchone()
            assert cust_row is not None, f"User {u.email} customer_id {u.customer_id} not found in MySQL!"
            assert cust_row[0] == u.customer_id

    conn.close()

def test_missing_or_invalid_customer_mapping():
    conn = get_mysql_conn()
    cursor = conn.cursor()
    
    cursor.execute("SELECT customer_id FROM customers WHERE customer_id = %s", ("CUST-NONEXISTENT",))
    assert cursor.fetchone() is None, "Non-existent customer_id returned data unexpectedly"
    
    conn.close()

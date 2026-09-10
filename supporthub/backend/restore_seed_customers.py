"""
restore_seed_customers.py
Restores the 25 canonical seed customers (CUST-001 to CUST-025) and all of their
associated business data (orders, order_items, payments, shipments, returns, refunds)
directly from the canonical supporthub_dump.sql dataset.
"""

import asyncio
import re
from datetime import datetime
from decimal import Decimal
import asyncpg
from pathlib import Path

DB_URL = 'postgresql://supporthub:supporthub_dev@127.0.0.1:5433/supporthub'
DUMP_PATH = Path(__file__).resolve().parents[2] / 'supporthub_dump.sql'

def parse_copy_table(content: str, table_name: str):
    pattern = rf'COPY public\.{table_name} \((.*?)\) FROM stdin;\n(.*?)\n\\\.'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find COPY section for public.{table_name}")
    cols = [c.strip() for c in match.group(1).split(',')]
    rows = []
    for line in match.group(2).strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        row_dict = {}
        for col, val in zip(cols, parts):
            row_dict[col] = None if val == r'\N' else val
        rows.append(row_dict)
    return cols, rows

async def restore():
    print(f"Loading dump from {DUMP_PATH}...")
    with open(DUMP_PATH, 'r', encoding='utf-8') as f:
        dump_content = f.read()

    conn = await asyncpg.connect(DB_URL)

    # 1. Parse canonical customers from dump
    _, all_users = parse_copy_table(dump_content, 'users')
    canonical_customers = {}
    for u in all_users:
        cid = u.get('customer_id')
        email = u.get('email') or ''
        if cid and cid.startswith('CUST-') and ('@example.com' in email or email == 'customer@supporthub.com'):
            if not email.startswith(('test_', 'cust2_', 'cust_', 'esc_')):
                canonical_customers[cid] = u

    print(f"Found {len(canonical_customers)} canonical seed customers (CUST-001 to CUST-025).")

    # 2. Restore customers
    print("\n=== Updating/Restoring 25 Seed Customers ===")
    for cid in sorted(canonical_customers.keys()):
        c = canonical_customers[cid]
        uid = c['id']
        email = c['email']
        name = c['name']
        phone = c['phone']
        address = c['address']
        city = c['city']
        state = c['state']
        postal_code = c['postal_code']
        country = c['country'] or 'India'
        company_id = c['company_id'] or 'COMP-001'
        pw_hash = c['password_hash']
        
        # Check if user with this email already exists
        existing_by_email = await conn.fetchrow("SELECT id FROM users WHERE email = $1", email)
        if existing_by_email:
            existing_id = str(existing_by_email['id'])
            if existing_id != uid:
                # Need to align UUID to canonical UUID. Delete the temporary random UUID record first.
                await conn.execute("DELETE FROM users WHERE id = $1", existing_by_email['id'])
                await conn.execute("""
                    INSERT INTO users (id, email, name, password_hash, role, status, phone, customer_id, address, city, state, postal_code, country, company_id, totp_enabled, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, 'customer', 'active', $5, $6, $7, $8, $9, $10, $11, $12, false, NOW(), NOW())
                """, uid, email, name, pw_hash, phone, cid, address, city, state, postal_code, country, company_id)
                print(f"  ✓ Replaced UUID & restored: {cid} | {name} ({email})")
            else:
                await conn.execute("""
                    UPDATE users SET name=$1, phone=$2, customer_id=$3, address=$4, city=$5, state=$6, postal_code=$7, country=$8, company_id=$9, updated_at=NOW()
                    WHERE id=$10
                """, name, phone, cid, address, city, state, postal_code, country, company_id, existing_by_email['id'])
                print(f"  ✓ Updated profile: {cid} | {name} ({email})")
        else:
            await conn.execute("""
                INSERT INTO users (id, email, name, password_hash, role, status, phone, customer_id, address, city, state, postal_code, country, company_id, totp_enabled, created_at, updated_at)
                VALUES ($1, $2, $3, $4, 'customer', 'active', $5, $6, $7, $8, $9, $10, $11, $12, false, NOW(), NOW())
            """, uid, email, name, pw_hash, phone, cid, address, city, state, postal_code, country, company_id)
            print(f"  + Inserted: {cid} | {name} ({email})")

    # 3. Restore Orders
    print("\n=== Restoring Orders ===")
    _, orders_data = parse_copy_table(dump_content, 'orders')
    for o in orders_data:
        order_date = datetime.fromisoformat(o['order_date']) if o['order_date'] else None
        created_at = datetime.fromisoformat(o['created_at']) if o['created_at'] else None
        updated_at = datetime.fromisoformat(o['updated_at']) if o['updated_at'] else None
        total_amount = Decimal(o['total_amount'])

        await conn.execute("""
            INSERT INTO orders (order_id, company_id, customer_id, status, order_date, total_amount, shipping_address, cancellation_reason, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ON CONFLICT (order_id) DO UPDATE SET
                company_id = EXCLUDED.company_id,
                customer_id = EXCLUDED.customer_id,
                status = EXCLUDED.status,
                order_date = EXCLUDED.order_date,
                total_amount = EXCLUDED.total_amount,
                shipping_address = EXCLUDED.shipping_address,
                cancellation_reason = EXCLUDED.cancellation_reason,
                updated_at = EXCLUDED.updated_at
        """, o['order_id'], o['company_id'], o['customer_id'], o['status'], order_date, total_amount,
             o['shipping_address'], o['cancellation_reason'], created_at, updated_at)
    print(f"  ✓ Restored {len(orders_data)} orders.")

    # 4. Restore Order Items
    print("\n=== Restoring Order Items ===")
    _, items_data = parse_copy_table(dump_content, 'order_items')
    for it in items_data:
        await conn.execute("""
            INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price, total_price)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (order_item_id) DO UPDATE SET
                order_id = EXCLUDED.order_id,
                product_id = EXCLUDED.product_id,
                quantity = EXCLUDED.quantity,
                unit_price = EXCLUDED.unit_price,
                total_price = EXCLUDED.total_price
        """, it['order_item_id'], it['order_id'], it['product_id'], int(it['quantity']),
             Decimal(it['unit_price']), Decimal(it['total_price']))
    print(f"  ✓ Restored {len(items_data)} order items.")

    # 5. Restore Payments
    print("\n=== Restoring Payments ===")
    _, payments_data = parse_copy_table(dump_content, 'payments')
    for p in payments_data:
        p_date = datetime.fromisoformat(p['payment_date']) if p['payment_date'] else None
        await conn.execute("""
            INSERT INTO payments (payment_id, order_id, customer_id, amount, method, status, transaction_reference, payment_date, failure_reason)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (payment_id) DO UPDATE SET
                order_id = EXCLUDED.order_id,
                customer_id = EXCLUDED.customer_id,
                amount = EXCLUDED.amount,
                method = EXCLUDED.method,
                status = EXCLUDED.status,
                transaction_reference = EXCLUDED.transaction_reference,
                payment_date = EXCLUDED.payment_date,
                failure_reason = EXCLUDED.failure_reason
        """, p['payment_id'], p['order_id'], p['customer_id'], Decimal(p['amount']),
             p['method'], p['status'], p['transaction_reference'], p_date, p['failure_reason'])
    print(f"  ✓ Restored {len(payments_data)} payments.")

    # 6. Restore Shipments
    print("\n=== Restoring Shipments ===")
    _, shipments_data = parse_copy_table(dump_content, 'shipments')
    for s in shipments_data:
        est_deliv = datetime.strptime(s['estimated_delivery_date'], '%Y-%m-%d').date() if s['estimated_delivery_date'] else None
        act_deliv = datetime.strptime(s['actual_delivery_date'], '%Y-%m-%d').date() if s['actual_delivery_date'] else None
        shipped_at = datetime.fromisoformat(s['shipped_at']) if s['shipped_at'] else None
        delivered_at = datetime.fromisoformat(s['delivered_at']) if s['delivered_at'] else None

        await conn.execute("""
            INSERT INTO shipments (shipment_id, order_id, tracking_number, carrier, status, estimated_delivery_date, actual_delivery_date, shipped_at, delivered_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (shipment_id) DO UPDATE SET
                order_id = EXCLUDED.order_id,
                tracking_number = EXCLUDED.tracking_number,
                carrier = EXCLUDED.carrier,
                status = EXCLUDED.status,
                estimated_delivery_date = EXCLUDED.estimated_delivery_date,
                actual_delivery_date = EXCLUDED.actual_delivery_date,
                shipped_at = EXCLUDED.shipped_at,
                delivered_at = EXCLUDED.delivered_at
        """, s['shipment_id'], s['order_id'], s['tracking_number'], s['carrier'], s['status'],
             est_deliv, act_deliv, shipped_at, delivered_at)
    print(f"  ✓ Restored {len(shipments_data)} shipments.")

    # 7. Restore Returns & Refunds
    print("\n=== Restoring Returns & Refunds ===")
    _, returns_data = parse_copy_table(dump_content, 'returns')
    for ret in returns_data:
        req_at = datetime.fromisoformat(ret['requested_at']) if ret['requested_at'] else None
        p_date = datetime.strptime(ret['pickup_date'], '%Y-%m-%d').date() if ret['pickup_date'] else None
        comp_at = datetime.fromisoformat(ret['completed_at']) if ret['completed_at'] else None

        await conn.execute("""
            INSERT INTO returns (return_id, order_id, order_item_id, customer_id, reason, status, requested_at, pickup_date, completed_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (return_id) DO UPDATE SET
                order_id = EXCLUDED.order_id,
                order_item_id = EXCLUDED.order_item_id,
                customer_id = EXCLUDED.customer_id,
                reason = EXCLUDED.reason,
                status = EXCLUDED.status,
                requested_at = EXCLUDED.requested_at,
                pickup_date = EXCLUDED.pickup_date,
                completed_at = EXCLUDED.completed_at
        """, ret['return_id'], ret['order_id'], ret['order_item_id'], ret['customer_id'],
             ret['reason'], ret['status'], req_at, p_date, comp_at)
    print(f"  ✓ Restored {len(returns_data)} returns.")

    _, refunds_data = parse_copy_table(dump_content, 'refunds')
    for rf in refunds_data:
        init_at = datetime.fromisoformat(rf['initiated_at']) if rf['initiated_at'] else None
        exp_date = datetime.strptime(rf['expected_date'], '%Y-%m-%d').date() if rf['expected_date'] else None
        comp_at = datetime.fromisoformat(rf['completed_at']) if rf['completed_at'] else None

        await conn.execute("""
            INSERT INTO refunds (refund_id, return_id, order_id, customer_id, refund_amount, status, initiated_at, expected_date, completed_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (refund_id) DO UPDATE SET
                return_id = EXCLUDED.return_id,
                order_id = EXCLUDED.order_id,
                customer_id = EXCLUDED.customer_id,
                refund_amount = EXCLUDED.refund_amount,
                status = EXCLUDED.status,
                initiated_at = EXCLUDED.initiated_at,
                expected_date = EXCLUDED.expected_date,
                completed_at = EXCLUDED.completed_at
        """, rf['refund_id'], rf['return_id'], rf['order_id'], rf['customer_id'],
             Decimal(rf['refund_amount']), rf['status'], init_at, exp_date, comp_at)
    print(f"  ✓ Restored {len(refunds_data)} refunds.")

    # 8. Summary Verification
    total_users = await conn.fetchval("SELECT count(*) FROM users")
    total_cust = await conn.fetchval("SELECT count(*) FROM users WHERE role='customer'")
    total_orders = await conn.fetchval("SELECT count(*) FROM orders")
    total_items = await conn.fetchval("SELECT count(*) FROM order_items")
    total_pay = await conn.fetchval("SELECT count(*) FROM payments")
    total_ship = await conn.fetchval("SELECT count(*) FROM shipments")
    total_ret = await conn.fetchval("SELECT count(*) FROM returns")
    total_ref = await conn.fetchval("SELECT count(*) FROM refunds")

    print("\n================ FINAL VERIFICATION ================")
    print(f"Total Users:      {total_users}")
    print(f"Total Customers:  {total_cust} (includes 25 seed + social profiles)")
    print(f"Total Orders:     {total_orders}")
    print(f"Total Order Items:{total_items}")
    print(f"Total Payments:   {total_pay}")
    print(f"Total Shipments:  {total_ship}")
    print(f"Total Returns:    {total_ret}")
    print(f"Total Refunds:    {total_ref}")

    print("\n25 Seed Customers:")
    seed_custs = await conn.fetch("""
        SELECT customer_id, name, email, phone, city, state, company_id 
        FROM users 
        WHERE customer_id IS NOT NULL 
        ORDER BY customer_id
    """)
    for row in seed_custs:
        print(f"  {row['customer_id']:8} | {row['name']:22} | {row['email']:28} | {row['phone']:18} | {row['city'] or '-'}")

    await conn.close()
    print("\n✅ Restore completed successfully!")

if __name__ == '__main__':
    asyncio.run(restore())

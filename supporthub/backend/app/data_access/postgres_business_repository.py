"""
PostgreSQL Repository for ShopKart Business Data Access.

Executes parameterized queries against the unified 'supporthub' PostgreSQL database,
mapping rows to domain dataclasses while enforcing customer scoping and ownership rules.
"""

import json
import logging
import uuid
from typing import Optional, List, Dict, Any
from app.data_access.base import (
    Company,
    Customer,
    Seller,
    Category,
    Product,
    Order,
    OrderItem,
    Payment,
    Shipment,
    Return,
    Refund,
    AccessDeniedError,
)
from app.data_access.db import mysql_db

logger = logging.getLogger(__name__)


def _to_str(val: Any) -> Optional[str]:
    if val is None:
        return None
    return str(val)


def _to_float(val: Any) -> float:
    if val is None:
        return 0.0
    return float(val)


def _to_int(val: Any) -> int:
    if val is None:
        return 0
    return int(val)


def _to_bool(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val == 1
    if isinstance(val, str):
        return val.lower() in ("true", "1", "yes", "t")
    return bool(val)


def _is_valid_uuid(val: Any) -> bool:
    if not val:
        return False
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, TypeError, AttributeError):
        return False


class PostgresBusinessRepository:
    """Repository handling all direct business data operations against PostgreSQL supporthub."""

    def __init__(self, db=None):
        self.db = db or mysql_db
        self._user_cust_cache: Dict[str, str] = {}

    def _resolve_customer_uuid(self, customer_id: str) -> Optional[str]:
        if not customer_id:
            return None
        if _is_valid_uuid(customer_id):
            return str(customer_id)
        with self.db.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE customer_id = %s LIMIT 1;", (customer_id,))
            row = cur.fetchone()
            if row:
                return str(row["id"])
        return None

    def _resolve_customer_string_id(self, user_id_val: Any) -> str:
        if not user_id_val:
            return ""
        s_val = str(user_id_val)
        if not _is_valid_uuid(s_val):
            return s_val
        if s_val in self._user_cust_cache:
            return self._user_cust_cache[s_val]
        with self.db.cursor() as cur:
            cur.execute("SELECT customer_id FROM users WHERE id = %s LIMIT 1;", (s_val,))
            row = cur.fetchone()
            if row and row.get("customer_id"):
                cust_id = row["customer_id"]
                self._user_cust_cache[s_val] = cust_id
                return cust_id
        return s_val

    # --- CUSTOMER ---
    def map_customer(self, row: Dict[str, Any]) -> Customer:
        full_name = row.get("name") or ""
        parts = full_name.split(" ", 1)
        first_name = row.get("first_name") or (parts[0] if parts else "")
        last_name = row.get("last_name") or (parts[1] if len(parts) > 1 else "")

        cust_id = row.get("customer_id") or str(row.get("id"))
        status = row.get("account_status")
        if not status:
            st = row.get("status")
            status = st.value.upper() if hasattr(st, "value") else str(st).upper() if st else "ACTIVE"

        return Customer(
            customer_id=cust_id,
            company_id=row.get("company_id") or "COMP-001",
            first_name=first_name,
            last_name=last_name,
            email=row.get("email", ""),
            phone=row.get("phone", "") or "",
            address=row.get("address", "") or "",
            city=row.get("city", "") or "",
            state=row.get("state", "") or "",
            postal_code=row.get("postal_code", "") or "",
            account_status=status,
            created_at=_to_str(row.get("created_at")),
        )

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        if not customer_id:
            return None
        with self.db.cursor() as cur:
            if _is_valid_uuid(customer_id):
                cur.execute("SELECT * FROM users WHERE id = %s LIMIT 1;", (customer_id,))
            else:
                cur.execute("SELECT * FROM users WHERE customer_id = %s LIMIT 1;", (customer_id,))
            row = cur.fetchone()
            return self.map_customer(row) if row else None

    def search_customer_by_phone(self, phone: str) -> Optional[Customer]:
        clean_phone = "".join(filter(str.isdigit, phone))
        if not clean_phone:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE phone IS NOT NULL;")
            rows = cur.fetchall()
            for row in rows:
                c_phone = "".join(filter(str.isdigit, row.get("phone", "") or ""))
                if c_phone and (c_phone == clean_phone or c_phone.endswith(clean_phone) or clean_phone.endswith(c_phone)):
                    return self.map_customer(row)
        return None

    def search_customer_by_email(self, email: str) -> Optional[Customer]:
        clean_email = email.strip().lower()
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = %s LIMIT 1;", (clean_email,))
            row = cur.fetchone()
            return self.map_customer(row) if row else None

    def list_all_customers(self) -> List[Customer]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE customer_id IS NOT NULL OR role::text = 'customer' ORDER BY customer_id, id;")
            rows = cur.fetchall()
            return [self.map_customer(r) for r in rows]

    # --- CATEGORY & SELLER ---
    def map_category(self, row: Dict[str, Any]) -> Category:
        return Category(
            category_id=row["category_id"],
            company_id=row["company_id"],
            name=row["name"],
            description=row.get("description", ""),
            parent_category_id=row.get("parent_category_id"),
        )

    def get_category(self, category_id: str) -> Optional[Category]:
        if not category_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE category_id = %s LIMIT 1;", (category_id,))
            row = cur.fetchone()
            return self.map_category(row) if row else None

    def map_seller(self, row: Dict[str, Any]) -> Seller:
        return Seller(
            seller_id=row["seller_id"],
            company_id=row["company_id"],
            seller_name=row["seller_name"],
            email=row.get("email", ""),
            phone=row.get("phone", ""),
            city=row.get("city", ""),
            state=row.get("state", ""),
            rating=_to_float(row.get("rating", 0.0)),
            status=row.get("status", "ACTIVE"),
        )

    def get_seller(self, seller_id: str) -> Optional[Seller]:
        if not seller_id:
            return None
        sid = seller_id.upper()
        if sid.startswith("SELLER-"):
            sid = sid.replace("SELLER-", "SELL-")
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM sellers WHERE seller_id = %s OR seller_id = %s LIMIT 1;", (sid, seller_id))
            row = cur.fetchone()
            return self.map_seller(row) if row else None

    def get_seller_by_product(self, product_id: str) -> Optional[Seller]:
        prod = self.get_product(product_id)
        if prod and prod.seller_id:
            return self.get_seller(prod.seller_id)
        return None

    def search_seller_by_name(self, name: str) -> Optional[Seller]:
        clean_name = f"%{name.strip().lower()}%"
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM sellers WHERE LOWER(seller_name) LIKE %s LIMIT 1;", (clean_name,))
            row = cur.fetchone()
            return self.map_seller(row) if row else None

    def list_all_sellers(self) -> List[Seller]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM sellers ORDER BY seller_id;")
            rows = cur.fetchall()
            return [self.map_seller(r) for r in rows]

    # --- PRODUCT ---
    def map_product(self, row: Dict[str, Any]) -> Product:
        specs = row.get("specifications")
        if isinstance(specs, str):
            try:
                specs = json.loads(specs)
            except Exception:
                specs = {}
        elif not isinstance(specs, dict):
            specs = {}

        return Product(
            product_id=row["product_id"],
            company_id=row["company_id"],
            seller_id=row["seller_id"],
            category_id=row["category_id"],
            name=row["name"],
            brand=row.get("brand", ""),
            description=row.get("description", ""),
            price=_to_float(row.get("price")),
            mrp=_to_float(row.get("mrp")),
            stock_quantity=_to_int(row.get("stock_quantity")),
            availability_status=row.get("availability_status", "IN_STOCK"),
            warranty_available=_to_bool(row.get("warranty_available")),
            warranty_period=row.get("warranty_period"),
            return_eligible=_to_bool(row.get("return_eligible", True)),
            return_window_days=_to_int(row.get("return_window_days", 7)),
            replacement_eligible=_to_bool(row.get("replacement_eligible", False)),
            specifications=specs,
        )

    def get_product(self, product_id: str) -> Optional[Product]:
        if not product_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE product_id = %s LIMIT 1;", (product_id,))
            row = cur.fetchone()
            return self.map_product(row) if row else None

    def search_products_by_name(self, query: str) -> List[Product]:
        clean_q = f"%{query.strip().lower()}%"
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT * FROM products WHERE LOWER(name) LIKE %s OR LOWER(brand) LIKE %s OR LOWER(description) LIKE %s;",
                (clean_q, clean_q, clean_q),
            )
            rows = cur.fetchall()
            return [self.map_product(r) for r in rows]

    def get_products_by_category(self, category_id: str) -> List[Product]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE category_id = %s;", (category_id,))
            rows = cur.fetchall()
            return [self.map_product(r) for r in rows]

    def list_all_products(self) -> List[Product]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM products ORDER BY product_id;")
            rows = cur.fetchall()
            return [self.map_product(r) for r in rows]

    # --- ORDER ---
    def map_order(self, row: Dict[str, Any]) -> Order:
        cust_str_id = self._resolve_customer_string_id(row["customer_id"])
        return Order(
            order_id=row["order_id"],
            company_id=row["company_id"],
            customer_id=cust_str_id,
            status=row["status"],
            order_date=_to_str(row["order_date"]),
            total_amount=_to_float(row["total_amount"]),
            shipping_address=row.get("shipping_address", ""),
            cancellation_reason=row.get("cancellation_reason"),
            cancelled_at=_to_str(row.get("cancelled_at")),
        )

    def get_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Order]:
        if not order_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE order_id = %s LIMIT 1;", (order_id,))
            row = cur.fetchone()
            if not row:
                return None
            order = self.map_order(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and order.customer_id != customer_id:
                    logger.warning(
                        "[OwnershipDenied] Customer '%s' attempted to access Order '%s' owned by '%s'",
                        customer_id,
                        order_id,
                        order.customer_id,
                    )
                    return None
            return order

    def get_customer_orders(self, customer_id: str) -> List[Order]:
        if not customer_id:
            return []
        c_uuid = self._resolve_customer_uuid(customer_id)
        if not c_uuid:
            return []
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC;", (c_uuid,))
            rows = cur.fetchall()
            return [self.map_order(r) for r in rows]

    def list_all_orders(self) -> List[Order]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM orders ORDER BY order_id;")
            rows = cur.fetchall()
            return [self.map_order(r) for r in rows]

    # --- ORDER ITEMS ---
    def map_order_item(self, row: Dict[str, Any]) -> OrderItem:
        return OrderItem(
            order_item_id=row["order_item_id"],
            order_id=row["order_id"],
            product_id=row["product_id"],
            quantity=_to_int(row["quantity"]),
            unit_price=_to_float(row["unit_price"]),
            total_price=_to_float(row["total_price"]),
        )

    def get_order_items(self, order_id: str, customer_id: Optional[str] = None) -> List[OrderItem]:
        order = self.get_order(order_id, customer_id=customer_id)
        if not order:
            return []
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM order_items WHERE order_id = %s;", (order_id,))
            rows = cur.fetchall()
            return [self.map_order_item(r) for r in rows]

    def list_all_order_items(self) -> List[OrderItem]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM order_items;")
            rows = cur.fetchall()
            return [self.map_order_item(r) for r in rows]


    def get_order_full_details(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        order = self.get_order(order_id, customer_id=customer_id)
        if not order:
            return None

        items = self.get_order_items(order_id)
        items_detail = []
        for item in items:
            product = self.get_product(item.product_id)
            items_detail.append({
                "order_item_id": item.order_item_id,
                "product_id": item.product_id,
                "product_name": product.name if product else "Unknown Product",
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            })

        shipment = self.get_shipment_by_order(order_id)
        payment = self.get_payment_by_order(order_id)

        return {
            "order": order,
            "items": items_detail,
            "shipment": shipment,
            "payment": payment,
        }

    # --- PAYMENT ---
    def map_payment(self, row: Dict[str, Any]) -> Payment:
        cust_str_id = self._resolve_customer_string_id(row["customer_id"])
        return Payment(
            payment_id=row["payment_id"],
            order_id=row["order_id"],
            customer_id=cust_str_id,
            amount=_to_float(row["amount"]),
            method=row["method"],
            status=row["status"],
            transaction_reference=row.get("transaction_reference", ""),
            payment_date=_to_str(row["payment_date"]),
            failure_reason=row.get("failure_reason"),
        )

    def get_payment(self, payment_id: str, customer_id: Optional[str] = None) -> Optional[Payment]:
        if not payment_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM payments WHERE payment_id = %s LIMIT 1;", (payment_id,))
            row = cur.fetchone()
            if not row:
                return None
            pay = self.map_payment(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and pay.customer_id != customer_id:
                    logger.warning("[OwnershipDenied] Customer '%s' attempted to access Payment '%s'", customer_id, payment_id)
                    return None
            return pay

    def get_payment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Payment]:
        if not order_id:
            return None
        order = self.get_order(order_id, customer_id=customer_id)
        if customer_id and not order:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM payments WHERE order_id = %s LIMIT 1;", (order_id,))
            row = cur.fetchone()
            if not row:
                return None
            pay = self.map_payment(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and pay.customer_id != customer_id:
                    return None
            return pay

    def get_customer_payments(self, customer_id: str) -> List[Payment]:
        if not customer_id:
            return []
        c_uuid = self._resolve_customer_uuid(customer_id)
        if not c_uuid:
            return []
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM payments WHERE customer_id = %s ORDER BY payment_date DESC;", (c_uuid,))
            rows = cur.fetchall()
            return [self.map_payment(r) for r in rows]

    def list_all_payments(self) -> List[Payment]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM payments ORDER BY payment_id;")
            rows = cur.fetchall()
            return [self.map_payment(r) for r in rows]

    # --- SHIPMENT ---
    def map_shipment(self, row: Dict[str, Any]) -> Shipment:
        return Shipment(
            shipment_id=row["shipment_id"],
            order_id=row["order_id"],
            tracking_number=row.get("tracking_number", "") or "",
            carrier=row.get("carrier", "") or "",
            status=row["status"],
            estimated_delivery_date=_to_str(row.get("estimated_delivery_date")),
            actual_delivery_date=_to_str(row.get("actual_delivery_date")),
            shipped_at=_to_str(row.get("shipped_at")),
            delay_reason=row.get("delay_reason"),
            delivery_address=row.get("delivery_address"),
        )

    def get_shipment(self, shipment_id: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        if not shipment_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM shipments WHERE shipment_id = %s LIMIT 1;", (shipment_id,))
            row = cur.fetchone()
            if not row:
                return None
            ship = self.map_shipment(row)
            if customer_id and customer_id != "ADMIN":
                order = self.get_order(ship.order_id, customer_id=customer_id)
                if not order:
                    logger.warning("[OwnershipDenied] Customer '%s' attempted to access Shipment '%s'", customer_id, shipment_id)
                    return None
            return ship

    def get_shipment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        if not order_id:
            return None
        order = self.get_order(order_id, customer_id=customer_id)
        if customer_id and not order:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM shipments WHERE order_id = %s LIMIT 1;", (order_id,))
            row = cur.fetchone()
            return self.map_shipment(row) if row else None

    def get_shipment_by_tracking(self, tracking_number: str, customer_id: Optional[str] = None) -> Optional[Shipment]:
        clean_num = tracking_number.strip().upper()
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM shipments WHERE UPPER(tracking_number) = %s LIMIT 1;", (clean_num,))
            row = cur.fetchone()
            if not row:
                return None
            ship = self.map_shipment(row)
            if customer_id and customer_id != "ADMIN":
                order = self.get_order(ship.order_id, customer_id=customer_id)
                if not order:
                    return None
            return ship

    def list_all_shipments(self) -> List[Shipment]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM shipments ORDER BY shipment_id;")
            rows = cur.fetchall()
            return [self.map_shipment(r) for r in rows]

    # --- RETURN ---
    def map_return(self, row: Dict[str, Any]) -> Return:
        cust_str_id = self._resolve_customer_string_id(row["customer_id"])
        return Return(
            return_id=row["return_id"],
            order_id=row["order_id"],
            order_item_id=row["order_item_id"],
            customer_id=cust_str_id,
            reason=row.get("reason", ""),
            status=row["status"],
            requested_at=_to_str(row["requested_at"]),
            pickup_date=_to_str(row.get("pickup_date")),
            completed_at=_to_str(row.get("completed_at")),
            rejection_reason=row.get("rejection_reason"),
        )

    def get_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Return]:
        if not return_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM returns WHERE return_id = %s LIMIT 1;", (return_id,))
            row = cur.fetchone()
            if not row:
                return None
            ret = self.map_return(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and ret.customer_id != customer_id:
                    logger.warning("[OwnershipDenied] Customer '%s' attempted to access Return '%s'", customer_id, return_id)
                    return None
            return ret

    def get_return_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Return]:
        if not order_id:
            return None
        order = self.get_order(order_id, customer_id=customer_id)
        if customer_id and not order:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM returns WHERE order_id = %s LIMIT 1;", (order_id,))
            row = cur.fetchone()
            if not row:
                return None
            ret = self.map_return(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and ret.customer_id != customer_id:
                    return None
            return ret

    def get_customer_returns(self, customer_id: str) -> List[Return]:
        if not customer_id:
            return []
        c_uuid = self._resolve_customer_uuid(customer_id)
        if not c_uuid:
            return []
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM returns WHERE customer_id = %s ORDER BY requested_at DESC;", (c_uuid,))
            rows = cur.fetchall()
            return [self.map_return(r) for r in rows]

    def list_all_returns(self) -> List[Return]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM returns ORDER BY return_id;")
            rows = cur.fetchall()
            return [self.map_return(r) for r in rows]

    # --- REFUND ---
    def map_refund(self, row: Dict[str, Any]) -> Refund:
        cust_str_id = self._resolve_customer_string_id(row["customer_id"])
        return Refund(
            refund_id=row["refund_id"],
            return_id=row.get("return_id"),
            order_id=row["order_id"],
            customer_id=cust_str_id,
            refund_amount=_to_float(row["refund_amount"]),
            status=row["status"],
            initiated_at=_to_str(row["initiated_at"]),
            expected_date=_to_str(row.get("expected_date")),
            completed_at=_to_str(row.get("completed_at")),
            failure_reason=row.get("failure_reason"),
            refund_method=row.get("refund_method"),
        )

    def get_refund(self, refund_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        if not refund_id:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM refunds WHERE refund_id = %s LIMIT 1;", (refund_id,))
            row = cur.fetchone()
            if not row:
                return None
            ref = self.map_refund(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and ref.customer_id != customer_id:
                    logger.warning("[OwnershipDenied] Customer '%s' attempted to access Refund '%s'", customer_id, refund_id)
                    return None
            return ref

    def get_refund_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        if not order_id:
            return None
        order = self.get_order(order_id, customer_id=customer_id)
        if customer_id and not order:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM refunds WHERE order_id = %s LIMIT 1;", (order_id,))
            row = cur.fetchone()
            if not row:
                return None
            ref = self.map_refund(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and ref.customer_id != customer_id:
                    return None
            return ref

    def get_refund_by_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Refund]:
        if not return_id:
            return None
        ret = self.get_return(return_id, customer_id=customer_id)
        if customer_id and not ret:
            return None
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM refunds WHERE return_id = %s LIMIT 1;", (return_id,))
            row = cur.fetchone()
            if not row:
                return None
            ref = self.map_refund(row)
            if customer_id and customer_id != "ADMIN":
                req_uuid = self._resolve_customer_uuid(customer_id)
                row_uuid = str(row["customer_id"])
                if req_uuid and req_uuid != row_uuid and ref.customer_id != customer_id:
                    return None
            return ref

    def get_customer_refunds(self, customer_id: str) -> List[Refund]:
        if not customer_id:
            return []
        c_uuid = self._resolve_customer_uuid(customer_id)
        if not c_uuid:
            return []
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM refunds WHERE customer_id = %s ORDER BY initiated_at DESC;", (c_uuid,))
            rows = cur.fetchall()
            return [self.map_refund(r) for r in rows]

    def list_all_refunds(self) -> List[Refund]:
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM refunds ORDER BY refund_id;")
            rows = cur.fetchall()
            return [self.map_refund(r) for r in rows]


# Singleton instance
postgres_business_repository = PostgresBusinessRepository()

# Backward compatibility aliases
MySQLRepository = PostgresBusinessRepository
mysql_repository = postgres_business_repository


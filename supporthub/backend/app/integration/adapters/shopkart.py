"""ShopKart business data adapter implementing the BusinessDataService contract."""
from typing import Optional, List, Dict, Any
from app.integration.contracts.business_data import BusinessDataService
from app.integration.security.tenant_boundary import TenantSecurityGuard
from app.data_access.customer_service import CustomerService
from app.data_access.product_service import ProductService
from app.data_access.seller_service import SellerService
from app.data_access.order_service import OrderService
from app.data_access.payment_service import PaymentService
from app.data_access.shipment_service import ShipmentService
from app.data_access.return_service import ReturnService
from app.data_access.refund_service import RefundService


class ShopKartBusinessDataAdapter(BusinessDataService):
    """
    Adapter bridging the synthetic ShopKart data services to the unified BusinessDataService contract.
    Enforces tenant scoping on all operations (ShopKart tenant ID: 'shopkart').
    """

    TENANT_ID = "shopkart"

    def __init__(self) -> None:
        self.customer_service = CustomerService()
        self.product_service = ProductService()
        self.seller_service = SellerService()
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.shipment_service = ShipmentService()
        self.return_service = ReturnService()
        self.refund_service = RefundService()

    def _verify_tenant(self, tenant_id: str) -> None:
        TenantSecurityGuard.validate_tenant_scope(
            requesting_tenant=tenant_id,
            entity_tenant=self.TENANT_ID,
            entity_type="ShopKart data store"
        )

    def get_customer(self, customer_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        cust = self.customer_service.get_customer(customer_id)
        if not cust:
            return None
        return {
            "customer_id": cust.customer_id,
            "tenant_id": self.TENANT_ID,
            "full_name": cust.full_name,
            "first_name": cust.first_name,
            "last_name": cust.last_name,
            "email": cust.email,
            "phone": cust.phone,
            "address": cust.address,
            "city": cust.city,
            "state": cust.state,
            "postal_code": cust.postal_code,
            "account_status": cust.account_status,
        }

    def get_product(self, product_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        prod = self.product_service.get_product(product_id)
        if not prod:
            return None
        return {
            "product_id": prod.product_id,
            "tenant_id": self.TENANT_ID,
            "title": prod.name,
            "name": prod.name,
            "brand": prod.brand,
            "category_id": prod.category_id,
            "price": prod.price,
            "mrp": prod.mrp,
            "stock_quantity": prod.stock_quantity,
            "warranty_period": prod.warranty_period,
            "return_window_days": prod.return_window_days,
            "specifications": prod.specifications,
        }

    def search_products(self, query: str, tenant_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        products = self.product_service.search_products_by_name(query)
        return [
            {
                "product_id": p.product_id,
                "tenant_id": self.TENANT_ID,
                "title": p.name,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "stock_quantity": p.stock_quantity,
            }
            for p in products
        ]

    def get_seller(self, seller_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        seller = self.seller_service.get_seller(seller_id)
        if not seller:
            return None
        return {
            "seller_id": seller.seller_id,
            "tenant_id": self.TENANT_ID,
            "name": seller.seller_name,
            "rating": seller.rating,
            "email": seller.email,
            "phone": seller.phone,
            "status": seller.status,
        }

    def get_order(self, order_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        order = self.order_service.get_order(order_id)
        if not order:
            return None
        return {
            "order_id": order.order_id,
            "tenant_id": self.TENANT_ID,
            "customer_id": order.customer_id,
            "order_date": order.order_date,
            "status": order.status,
            "total_amount": order.total_amount,
            "shipping_address": order.shipping_address,
        }

    def get_customer_orders(self, customer_id: str, tenant_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        orders = self.order_service.get_customer_orders(customer_id)
        return [
            {
                "order_id": o.order_id,
                "tenant_id": self.TENANT_ID,
                "customer_id": o.customer_id,
                "order_date": o.order_date,
                "status": o.status,
                "total_amount": o.total_amount,
            }
            for o in orders[:limit]
        ]

    def get_order_items(self, order_id: str, tenant_id: str) -> List[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        items = self.order_service.get_order_items(order_id)
        return [
            {
                "order_item_id": it.order_item_id,
                "order_id": it.order_id,
                "product_id": it.product_id,
                "quantity": it.quantity,
                "unit_price": it.unit_price,
                "total_price": it.total_price,
            }
            for it in items
        ]

    def get_payment(self, payment_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        pay = self.payment_service.get_payment(payment_id)
        if not pay:
            return None
        return {
            "payment_id": pay.payment_id,
            "tenant_id": self.TENANT_ID,
            "order_id": pay.order_id,
            "customer_id": pay.customer_id,
            "method": pay.method,
            "amount": pay.amount,
            "status": pay.status,
            "transaction_reference": pay.transaction_reference,
            "payment_date": pay.payment_date,
        }

    def get_shipment(self, shipment_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        ship = self.shipment_service.get_shipment(shipment_id)
        if not ship:
            return None
        return {
            "shipment_id": ship.shipment_id,
            "tenant_id": self.TENANT_ID,
            "order_id": ship.order_id,
            "carrier": ship.carrier,
            "tracking_number": ship.tracking_number,
            "status": ship.status,
            "estimated_delivery_date": ship.estimated_delivery_date,
            "actual_delivery_date": ship.actual_delivery_date,
            "delivery_address": ship.delivery_address,
        }

    def get_return(self, return_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        ret = self.return_service.get_return(return_id)
        if not ret:
            return None
        return {
            "return_id": ret.return_id,
            "tenant_id": self.TENANT_ID,
            "order_id": ret.order_id,
            "customer_id": ret.customer_id,
            "reason": ret.reason,
            "status": ret.status,
            "requested_at": ret.requested_at,
            "pickup_date": ret.pickup_date,
        }

    def get_refund(self, refund_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        self._verify_tenant(tenant_id)
        ref = self.refund_service.get_refund(refund_id)
        if not ref:
            return None
        return {
            "refund_id": ref.refund_id,
            "tenant_id": self.TENANT_ID,
            "order_id": ref.order_id,
            "return_id": ref.return_id,
            "customer_id": ref.customer_id,
            "refund_amount": ref.refund_amount,
            "status": ref.status,
            "initiated_at": ref.initiated_at,
            "expected_date": ref.expected_date,
            "completed_at": ref.completed_at,
            "refund_method": ref.refund_method,
        }

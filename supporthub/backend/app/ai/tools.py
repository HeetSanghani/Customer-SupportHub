"""Tool registry wrapping structured data access services."""
from typing import Dict, Any, Optional, Callable
from app.data_access.customer_service import CustomerService
from app.data_access.product_service import ProductService
from app.data_access.seller_service import SellerService
from app.data_access.order_service import OrderService
from app.data_access.payment_service import PaymentService
from app.data_access.shipment_service import ShipmentService
from app.data_access.return_service import ReturnService
from app.data_access.refund_service import RefundService


class ToolRegistry:
    """Provides validated tool calling interfaces for the AI Orchestrator."""

    def __init__(
        self,
        customer_service: Optional[CustomerService] = None,
        product_service: Optional[ProductService] = None,
        seller_service: Optional[SellerService] = None,
        order_service: Optional[OrderService] = None,
        payment_service: Optional[PaymentService] = None,
        shipment_service: Optional[ShipmentService] = None,
        return_service: Optional[ReturnService] = None,
        refund_service: Optional[RefundService] = None
    ):
        from app.data_access.loader import data_loader
        self.customer_svc = customer_service or CustomerService(loader=data_loader)
        self.product_svc = product_service or ProductService(loader=data_loader)
        self.seller_svc = seller_service or SellerService(loader=data_loader)
        self.order_svc = order_service or OrderService(loader=data_loader)
        self.payment_svc = payment_service or PaymentService(loader=data_loader)
        self.shipment_svc = shipment_service or ShipmentService(loader=data_loader)
        self.return_svc = return_service or ReturnService(loader=data_loader)
        self.refund_svc = refund_service or RefundService(loader=data_loader)

        # Tool mapping
        self._tools: Dict[str, Callable] = {
            "get_customer": self.get_customer,
            "get_product": self.get_product,
            "search_products": self.search_products,
            "list_all_products": self.list_all_products,
            "get_seller": self.get_seller,
            "get_seller_by_product": self.get_seller_by_product,
            "get_order": self.get_order,
            "get_order_items": self.get_order_items,
            "get_order_full_details": self.get_order_full_details,
            "get_customer_orders": self.get_customer_orders,
            "get_payment_by_order": self.get_payment_by_order,
            "get_payment": self.get_payment,
            "get_shipment_by_order": self.get_shipment_by_order,
            "get_shipment_by_tracking": self.get_shipment_by_tracking,
            "get_return": self.get_return,
            "get_return_by_order": self.get_return_by_order,
            "get_refund": self.get_refund,
            "get_refund_by_order": self.get_refund_by_order,
            "get_refund_by_return": self.get_refund_by_return,
        }

    def execute(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool by name with arguments."""
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' is not registered in ToolRegistry.")
        return self._tools[tool_name](**kwargs)

    # Tool Implementations
    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        c = self.customer_svc.get_customer(customer_id)
        if not c:
            return None
        return {
            "customer_id": c.customer_id,
            "name": c.full_name,
            "email": c.email,
            "phone": c.phone,
            "city": c.city,
            "state": c.state,
            "account_status": c.account_status
        }

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        p = self.product_svc.get_product(product_id)
        if not p:
            return None
        cat = self.product_svc.get_category(p.category_id)
        return {
            "product_id": p.product_id,
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "mrp": p.mrp,
            "discount_percentage": p.discount_percentage,
            "stock_quantity": p.stock_quantity,
            "availability_status": p.availability_status,
            "warranty_available": p.warranty_available,
            "warranty_period": p.warranty_period,
            "return_eligible": p.return_eligible,
            "return_window_days": p.return_window_days,
            "replacement_eligible": p.replacement_eligible,
            "category_id": p.category_id,
            "category_name": cat.name if cat else "General",
            "specifications": p.specifications,
            "seller_id": p.seller_id
        }

    def search_products(self, query: str) -> list:
        prods = self.product_svc.search_products_by_name(query)
        res = []
        for p in prods[:8]:
            cat = self.product_svc.get_category(p.category_id)
            res.append({
                "product_id": p.product_id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "mrp": p.mrp,
                "discount_percentage": p.discount_percentage,
                "category_id": p.category_id,
                "category_name": cat.name if cat else "General",
                "stock_quantity": p.stock_quantity,
                "availability_status": p.availability_status,
                "warranty_period": p.warranty_period,
                "return_window_days": p.return_window_days
            })
        return res

    def list_all_products(self, limit: int = 40) -> list:
        prods = self.product_svc.list_all_products()
        res = []
        for p in prods[:limit]:
            cat = self.product_svc.get_category(p.category_id)
            res.append({
                "product_id": p.product_id,
                "name": p.name,
                "brand": p.brand,
                "price": p.price,
                "mrp": p.mrp,
                "discount_percentage": p.discount_percentage,
                "category_id": p.category_id,
                "category_name": cat.name if cat else "General",
                "stock_quantity": p.stock_quantity,
                "availability_status": p.availability_status,
                "warranty_period": p.warranty_period,
                "return_window_days": p.return_window_days
            })
        return res

    def get_seller(self, seller_id: str) -> Optional[Dict[str, Any]]:
        s = self.seller_svc.get_seller(seller_id)
        if not s:
            return None
        return {
            "seller_id": s.seller_id,
            "seller_name": s.seller_name,
            "rating": s.rating,
            "city": s.city,
            "state": s.state,
            "status": s.status
        }

    def get_seller_by_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        s = self.seller_svc.get_seller_by_product(product_id)
        if not s:
            return None
        return {
            "seller_id": s.seller_id,
            "seller_name": s.seller_name,
            "rating": s.rating,
            "city": s.city,
            "state": s.state
        }

    def get_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        o = self.order_svc.get_order(order_id, customer_id=customer_id)
        if not o:
            return None
        return {
            "order_id": o.order_id,
            "customer_id": o.customer_id,
            "status": o.status,
            "order_date": o.order_date,
            "total_amount": o.total_amount,
            "shipping_address": o.shipping_address,
            "cancellation_reason": o.cancellation_reason,
            "cancelled_at": o.cancelled_at
        }

    def get_order_items(self, order_id: str, customer_id: Optional[str] = None) -> list:
        items = self.order_svc.get_order_items(order_id, customer_id=customer_id)
        res = []
        for item in items:
            p = self.product_svc.get_product(item.product_id)
            res.append({
                "order_item_id": item.order_item_id,
                "product_id": item.product_id,
                "product_name": p.name if p else "Product",
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price
            })
        return res

    def get_order_full_details(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        return self.order_svc.get_order_full_details(order_id, customer_id=customer_id)

    def get_customer_orders(self, customer_id: str) -> list:
        orders = self.order_svc.get_customer_orders(customer_id)
        return [
            {
                "order_id": o.order_id,
                "customer_id": o.customer_id,
                "status": o.status,
                "order_date": o.order_date,
                "total_amount": o.total_amount,
                "shipping_address": o.shipping_address,
                "cancellation_reason": o.cancellation_reason,
                "cancelled_at": o.cancelled_at
            }
            for o in orders
        ]

    def get_payment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        p = self.payment_svc.get_payment_by_order(order_id, customer_id=customer_id)
        if not p:
            return None
        return {
            "payment_id": p.payment_id,
            "order_id": p.order_id,
            "customer_id": p.customer_id,
            "amount": p.amount,
            "method": p.method,
            "status": p.status,
            "transaction_reference": p.transaction_reference,
            "payment_date": p.payment_date,
            "failure_reason": p.failure_reason
        }

    def get_payment(self, payment_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        p = self.payment_svc.get_payment(payment_id, customer_id=customer_id)
        if not p:
            return None
        return {
            "payment_id": p.payment_id,
            "order_id": p.order_id,
            "customer_id": p.customer_id,
            "amount": p.amount,
            "method": p.method,
            "status": p.status,
            "transaction_reference": p.transaction_reference,
            "failure_reason": p.failure_reason
        }

    def get_shipment_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        s = self.shipment_svc.get_shipment_by_order(order_id, customer_id=customer_id)
        if not s:
            return None
        return {
            "shipment_id": s.shipment_id,
            "order_id": s.order_id,
            "tracking_number": s.tracking_number,
            "carrier": s.carrier,
            "status": s.status,
            "estimated_delivery_date": s.estimated_delivery_date,
            "actual_delivery_date": s.actual_delivery_date,
            "delay_reason": s.delay_reason
        }

    def get_shipment_by_tracking(self, tracking_number: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        s = self.shipment_svc.get_shipment_by_tracking(tracking_number, customer_id=customer_id)
        if not s:
            return None
        return {
            "shipment_id": s.shipment_id,
            "order_id": s.order_id,
            "tracking_number": s.tracking_number,
            "carrier": s.carrier,
            "status": s.status,
            "estimated_delivery_date": s.estimated_delivery_date,
            "actual_delivery_date": s.actual_delivery_date
        }

    def get_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        r = self.return_svc.get_return(return_id, customer_id=customer_id)
        if not r:
            return None
        return {
            "return_id": r.return_id,
            "order_id": r.order_id,
            "customer_id": r.customer_id,
            "status": r.status,
            "reason": r.reason,
            "requested_at": r.requested_at,
            "pickup_date": r.pickup_date,
            "rejection_reason": r.rejection_reason
        }

    def get_return_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        r = self.return_svc.get_return_by_order(order_id, customer_id=customer_id)
        if not r:
            return None
        return {
            "return_id": r.return_id,
            "order_id": r.order_id,
            "customer_id": r.customer_id,
            "status": r.status,
            "reason": r.reason,
            "pickup_date": r.pickup_date,
            "rejection_reason": r.rejection_reason
        }

    def get_refund(self, refund_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        ref = self.refund_svc.get_refund(refund_id, customer_id=customer_id)
        if not ref:
            return None
        return {
            "refund_id": ref.refund_id,
            "order_id": ref.order_id,
            "customer_id": ref.customer_id,
            "refund_amount": ref.refund_amount,
            "status": ref.status,
            "refund_method": ref.refund_method,
            "expected_date": ref.expected_date,
            "completed_at": ref.completed_at,
            "failure_reason": ref.failure_reason
        }

    def get_refund_by_order(self, order_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        ref = self.refund_svc.get_refund_by_order(order_id, customer_id=customer_id)
        if not ref:
            return None
        return {
            "refund_id": ref.refund_id,
            "order_id": ref.order_id,
            "customer_id": ref.customer_id,
            "refund_amount": ref.refund_amount,
            "status": ref.status,
            "refund_method": ref.refund_method,
            "expected_date": ref.expected_date,
            "completed_at": ref.completed_at,
            "failure_reason": ref.failure_reason
        }

    def get_refund_by_return(self, return_id: str, customer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        ref = self.refund_svc.get_refund_by_return(return_id, customer_id=customer_id)
        if not ref:
            return None
        return {
            "refund_id": ref.refund_id,
            "return_id": ref.return_id,
            "order_id": ref.order_id,
            "refund_amount": ref.refund_amount,
            "status": ref.status,
            "refund_method": ref.refund_method,
            "expected_date": ref.expected_date
        }


tool_registry = ToolRegistry()

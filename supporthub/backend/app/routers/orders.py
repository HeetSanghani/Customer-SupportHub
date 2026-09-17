"""
app/routers/orders.py

Customer Orders & Transactional Data Router.
All endpoints derive caller identity strictly from authenticated JWT current_user.
Query parameters or body claims for customer_id are NEVER accepted or trusted.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_current_user
from app.models import User, UserRole
from app.database import get_session
from app.data_access.order_service import OrderService
from app.data_access.shipment_service import ShipmentService
from app.data_access.return_service import ReturnService
from app.data_access.refund_service import RefundService
from app.data_access.payment_service import PaymentService

router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderService()
shipment_service = ShipmentService()
return_service = ReturnService()
refund_service = RefundService()
payment_service = PaymentService()


def get_effective_customer_id(user: User) -> str:
    """Return the authenticated customer's customer_id string (e.g. CUST-001) or UUID string."""
    return user.customer_id or str(user.id)


# ─── Pydantic Response Schemas ────────────────────────────────────────────────

class OrderSummary(BaseModel):
    order_id: str
    company_id: Optional[str] = None
    customer_id: str
    status: str
    order_date: Optional[str] = None
    total_amount: float
    shipping_address: Optional[str] = None
    cancellation_reason: Optional[str] = None


class OrderItemDetail(BaseModel):
    order_item_id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float


class ShipmentDetail(BaseModel):
    shipment_id: str
    order_id: str
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    status: str
    estimated_delivery_date: Optional[str] = None
    actual_delivery_date: Optional[str] = None


class PaymentDetail(BaseModel):
    payment_id: str
    order_id: str
    amount: float
    method: str
    status: str
    payment_date: Optional[str] = None


class OrderFullDetailResponse(BaseModel):
    order: OrderSummary
    items: List[OrderItemDetail]
    shipment: Optional[ShipmentDetail] = None
    payment: Optional[PaymentDetail] = None


class ReturnDetail(BaseModel):
    return_id: str
    order_id: str
    order_item_id: str
    customer_id: str
    reason: str
    status: str
    requested_at: Optional[str] = None


class RefundDetail(BaseModel):
    refund_id: str
    return_id: str
    order_id: str
    customer_id: str
    refund_amount: float
    status: str
    initiated_at: Optional[str] = None


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.get("/me", response_model=List[OrderSummary])
async def get_my_orders(current_user: User = Depends(get_current_user)):
    """Fetch all orders belonging to the authenticated customer."""
    cust_id = get_effective_customer_id(current_user)
    orders = order_service.get_customer_orders(cust_id)
    return [
        OrderSummary(
            order_id=o.order_id,
            company_id=o.company_id,
            customer_id=o.customer_id,
            status=o.status,
            order_date=str(o.order_date) if o.order_date else None,
            total_amount=float(o.total_amount) if o.total_amount is not None else 0.0,
            shipping_address=o.shipping_address,
            cancellation_reason=o.cancellation_reason,
        ) for o in orders
    ]


@router.get("/shipments/me", response_model=List[ShipmentDetail])
async def get_my_shipments(current_user: User = Depends(get_current_user)):
    """Fetch all shipments belonging to the authenticated customer's orders."""
    cust_id = get_effective_customer_id(current_user)
    orders = order_service.get_customer_orders(cust_id)
    shipments: List[ShipmentDetail] = []
    for o in orders:
        s = shipment_service.get_shipment_by_order(o.order_id, customer_id=cust_id)
        if s:
            shipments.append(
                ShipmentDetail(
                    shipment_id=s.shipment_id,
                    order_id=s.order_id,
                    tracking_number=s.tracking_number,
                    carrier=s.carrier,
                    status=s.status,
                    estimated_delivery_date=str(s.estimated_delivery_date) if s.estimated_delivery_date else None,
                    actual_delivery_date=str(s.actual_delivery_date) if s.actual_delivery_date else None,
                )
            )
    return shipments


@router.get("/returns/me", response_model=List[ReturnDetail])
async def get_my_returns(current_user: User = Depends(get_current_user)):
    """Fetch all returns belonging to the authenticated customer."""
    cust_id = get_effective_customer_id(current_user)
    returns = return_service.get_customer_returns(cust_id)
    return [
        ReturnDetail(
            return_id=r.return_id,
            order_id=r.order_id,
            order_item_id=r.order_item_id,
            customer_id=r.customer_id,
            reason=r.reason,
            status=r.status,
            requested_at=str(r.requested_at) if r.requested_at else None,
        ) for r in returns
    ]


@router.get("/refunds/me", response_model=List[RefundDetail])
async def get_my_refunds(current_user: User = Depends(get_current_user)):
    """Fetch all refunds belonging to the authenticated customer."""
    cust_id = get_effective_customer_id(current_user)
    refunds = refund_service.get_customer_refunds(cust_id)
    return [
        RefundDetail(
            refund_id=rf.refund_id,
            return_id=rf.return_id,
            order_id=rf.order_id,
            customer_id=rf.customer_id,
            refund_amount=float(rf.refund_amount) if rf.refund_amount is not None else 0.0,
            status=rf.status,
            initiated_at=str(rf.initiated_at) if rf.initiated_at else None,
        ) for rf in refunds
    ]


@router.get("/payments/me", response_model=List[PaymentDetail])
async def get_my_payments(current_user: User = Depends(get_current_user)):
    """Fetch all safe payment summaries belonging to the authenticated customer's orders."""
    cust_id = get_effective_customer_id(current_user)
    payments = payment_service.get_customer_payments(cust_id)
    return [
        PaymentDetail(
            payment_id=p.payment_id,
            order_id=p.order_id,
            amount=float(p.amount) if p.amount is not None else 0.0,
            method=p.method,
            status=p.status,
            payment_date=str(p.payment_date) if p.payment_date else None,
        ) for p in payments
    ]


# ─── Staff-Only: Fetch orders for a customer by their User UUID ───────────────

class OrderSummaryWithShipment(BaseModel):
    order_id: str
    customer_id: str
    status: str
    order_date: Optional[str] = None
    total_amount: float
    items: List[OrderItemDetail] = []
    shipment_status: Optional[str] = None
    shipment_carrier: Optional[str] = None
    estimated_delivery_date: Optional[str] = None
    actual_delivery_date: Optional[str] = None
    payment_status: Optional[str] = None


@router.get("/by-customer/{user_id}", response_model=List[OrderSummaryWithShipment])
async def get_orders_for_customer(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Staff-only: Fetch all orders for a customer by their User UUID (ticket.customer_id)."""
    if current_user.role not in (UserRole.agent, UserRole.manager, UserRole.admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Resolve the user to get their business customer_id (e.g. CUST-001)
    try:
        import uuid as _uuid
        uid = _uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user_id format")

    target_user = await session.get(User, uid)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Use the business customer_id (e.g. CUST-001) or fall back to UUID string
    cust_id = target_user.customer_id or str(target_user.id)

    orders = order_service.get_customer_orders(cust_id)
    result_list: List[OrderSummaryWithShipment] = []

    for o in orders:
        # Use get_order_full_details to get items with product names (returns dict list)
        details = order_service.get_order_full_details(o.order_id)
        items_dicts = details.get("items", []) if details else []
        items = [
            OrderItemDetail(
                order_item_id=i["order_item_id"],
                product_id=i["product_id"],
                product_name=i.get("product_name", "Unknown"),
                quantity=i["quantity"],
                unit_price=float(i["unit_price"]),
                total_price=float(i["total_price"]),
            )
            for i in items_dicts
        ]

        # Shipment & payment already fetched in full details
        shipment = details.get("shipment") if details else None
        payment = details.get("payment") if details else None

        result_list.append(
            OrderSummaryWithShipment(
                order_id=o.order_id,
                customer_id=o.customer_id,
                status=o.status,
                order_date=str(o.order_date) if o.order_date else None,
                total_amount=float(o.total_amount) if o.total_amount is not None else 0.0,
                items=items,
                shipment_status=shipment.status if shipment else None,
                shipment_carrier=shipment.carrier if shipment else None,
                estimated_delivery_date=str(shipment.estimated_delivery_date) if shipment and shipment.estimated_delivery_date else None,
                actual_delivery_date=str(shipment.actual_delivery_date) if shipment and shipment.actual_delivery_date else None,
                payment_status=payment.status if payment else None,
            )
        )

    return result_list


@router.get("/{order_id}", response_model=OrderFullDetailResponse)
async def get_order_detail(order_id: str, current_user: User = Depends(get_current_user)):
    """Fetch order details if owned by caller (or if caller is staff)."""
    cust_id = get_effective_customer_id(current_user)
    
    # Staff override
    check_cust_id = None if current_user.role in (UserRole.agent, UserRole.manager, UserRole.admin) else cust_id
    
    details = order_service.get_order_full_details(order_id, customer_id=check_cust_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or unauthorized"
        )
    
    order_obj = details["order"]
    items_objs = details.get("items", [])
    shipment_obj = details.get("shipment")
    payment_obj = details.get("payment")

    return OrderFullDetailResponse(
        order=OrderSummary(
            order_id=order_obj.order_id,
            company_id=order_obj.company_id,
            customer_id=order_obj.customer_id,
            status=order_obj.status,
            order_date=str(order_obj.order_date) if order_obj.order_date else None,
            total_amount=float(order_obj.total_amount) if order_obj.total_amount is not None else 0.0,
            shipping_address=order_obj.shipping_address,
            cancellation_reason=order_obj.cancellation_reason,
        ),
        items=[
            OrderItemDetail(
                order_item_id=i["order_item_id"],
                product_id=i["product_id"],
                product_name=i["product_name"],
                quantity=i["quantity"],
                unit_price=float(i["unit_price"]),
                total_price=float(i["total_price"]),
            ) for i in items_objs
        ],
        shipment=ShipmentDetail(
            shipment_id=shipment_obj.shipment_id,
            order_id=shipment_obj.order_id,
            tracking_number=shipment_obj.tracking_number,
            carrier=shipment_obj.carrier,
            status=shipment_obj.status,
            estimated_delivery_date=str(shipment_obj.estimated_delivery_date) if shipment_obj.estimated_delivery_date else None,
            actual_delivery_date=str(shipment_obj.actual_delivery_date) if shipment_obj.actual_delivery_date else None,
        ) if shipment_obj else None,
        payment=PaymentDetail(
            payment_id=payment_obj.payment_id,
            order_id=payment_obj.order_id,
            amount=float(payment_obj.amount),
            method=payment_obj.method,
            status=payment_obj.status,
            payment_date=str(payment_obj.payment_date) if payment_obj.payment_date else None,
        ) if payment_obj else None,
    )

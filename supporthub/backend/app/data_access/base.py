"""Base dataclasses and exceptions for Structured Data Access layer."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# Custom Exceptions
class DataAccessException(Exception):
    """Base exception for all data access errors."""
    pass


class EntityNotFoundError(DataAccessException):
    """Raised when a requested entity record is not found."""
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with ID '{entity_id}' not found.")


class AccessDeniedError(DataAccessException):
    """Raised when a caller attempts unauthorized cross-customer access."""
    def __init__(self, message: str = "Access denied: Unauthorized resource ownership."):
        super().__init__(message)


class ValidationError(DataAccessException):
    """Raised when input parameters fail format or domain constraints."""
    pass


# Domain Dataclasses
@dataclass
class Company:
    company_id: str
    name: str
    description: str
    website: str
    support_email: str
    support_phone: str
    default_currency: str
    country: str
    timezone: str
    status: str


@dataclass
class Customer:
    customer_id: str
    company_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    postal_code: str
    account_status: str
    created_at: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Seller:
    seller_id: str
    company_id: str
    seller_name: str
    email: str
    phone: str
    city: str
    state: str
    rating: float
    status: str


@dataclass
class Category:
    category_id: str
    company_id: str
    name: str
    description: str
    parent_category_id: Optional[str] = None


@dataclass
class Product:
    product_id: str
    company_id: str
    seller_id: str
    category_id: str
    name: str
    brand: str
    description: str
    price: float
    mrp: float
    stock_quantity: int
    availability_status: str
    warranty_available: bool
    warranty_period: Optional[str] = None
    return_eligible: bool = True
    return_window_days: int = 7
    replacement_eligible: bool = False
    specifications: Dict[str, Any] = field(default_factory=dict)

    @property
    def discount_percentage(self) -> float:
        if self.mrp > 0 and self.mrp > self.price:
            return round(((self.mrp - self.price) / self.mrp) * 100, 1)
        return 0.0


@dataclass
class OrderItem:
    order_item_id: str
    order_id: str
    product_id: str
    quantity: int
    unit_price: float
    total_price: float


@dataclass
class Order:
    order_id: str
    company_id: str
    customer_id: str
    status: str
    order_date: str
    total_amount: float
    shipping_address: str
    cancellation_reason: Optional[str] = None
    cancelled_at: Optional[str] = None


@dataclass
class Payment:
    payment_id: str
    order_id: str
    customer_id: str
    amount: float
    method: str
    status: str
    transaction_reference: str
    payment_date: str
    failure_reason: Optional[str] = None


@dataclass
class Shipment:
    shipment_id: str
    order_id: str
    tracking_number: str
    carrier: str
    status: str
    estimated_delivery_date: Optional[str] = None
    actual_delivery_date: Optional[str] = None
    shipped_at: Optional[str] = None
    delay_reason: Optional[str] = None
    delivery_address: Optional[str] = None


@dataclass
class Return:
    return_id: str
    order_id: str
    order_item_id: str
    customer_id: str
    reason: str
    status: str
    requested_at: str
    pickup_date: Optional[str] = None
    completed_at: Optional[str] = None
    rejection_reason: Optional[str] = None


@dataclass
class Refund:
    refund_id: str
    return_id: Optional[str]
    order_id: str
    customer_id: str
    refund_amount: float
    status: str
    initiated_at: str
    expected_date: Optional[str] = None
    completed_at: Optional[str] = None
    failure_reason: Optional[str] = None
    refund_method: Optional[str] = None

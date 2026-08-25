# 05. Proposed MySQL Schema Design

## DDL Schema Draft

```sql
CREATE TABLE company (
    company_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    support_email VARCHAR(255),
    support_phone VARCHAR(50),
    default_currency VARCHAR(10) DEFAULT 'USD',
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_category_id VARCHAR(50),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    seller_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    rating DECIMAL(3,2),
    joined_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    category_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    specifications JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    company_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    order_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    INDEX idx_orders_customer (customer_id)
);

CREATE TABLE order_items (
    order_item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    transaction_reference VARCHAR(100),
    payment_date TIMESTAMP NOT NULL,
    failure_reason TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(100),
    carrier VARCHAR(100),
    status VARCHAR(50) NOT NULL,
    estimated_delivery_date DATE,
    actual_delivery_date DATE,
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE returns (
    return_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_item_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pickup_date DATE,
    completed_at TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE refunds (
    refund_id VARCHAR(50) PRIMARY KEY,
    return_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    refund_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_date DATE,
    completed_at TIMESTAMP,
    FOREIGN KEY (return_id) REFERENCES returns(return_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

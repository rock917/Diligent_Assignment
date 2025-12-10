# E-Commerce Database Project

A complete e-commerce database system using synthetic data for SQL practice and database management. This project generates realistic fake e-commerce data, imports it into SQLite, and provides query scripts for analysis.

## 📋 Project Overview

This project creates a realistic e-commerce database system with synthetic data that mimics real-world patterns without using any actual customer information. It includes:

- **Data Generation**: Python scripts to create synthetic e-commerce data
- **Database Import**: Automated import of CSV files into SQLite database
- **Query Scripts**: Pre-built SQL queries for customer analysis

## 🗂️ Project Structure

```
bobby/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── prompt.txt                     # Original project requirements
│
├── Data Generation:
├── generate_ecommerce_data.py     # Generates initial CSV files (customers, products, orders, order_items, categories)
├── create_payments.py             # Generates payments.csv and imports to database
│
├── Database Import:
├── import_to_sqlite.py            # Imports all CSV files into SQLite database
│
├── Query Scripts:
├── customer_order_summary.py      # Main query: customer orders and spending analysis
├── verify_db.py                   # Database verification and sample queries
│
├── CSV Files:
├── customers.csv                  # Customer information (500 records)
├── products.csv                   # Product catalog (200 records)
├── categories.csv                 # Product categories (15 records)
├── orders.csv                     # Order headers (1,000 records)
├── order_items.csv                # Order line items (3,020 records)
├── payments.csv                   # Payment transactions (1,055 records)
│
└── Database:
    └── ecom.db                    # SQLite database (created after import)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `Faker` - For generating realistic synthetic data

### Step 1: Generate Data (Optional)

If you want to regenerate the CSV files from scratch:

```bash
python generate_ecommerce_data.py
```

This creates:
- `categories.csv` (15 categories)
- `products.csv` (200 products)
- `customers.csv` (500 customers)
- `orders.csv` (1,000 orders)
- `order_items.csv` (3,020 order items)

### Step 2: Create Payments Data

Generate and import payments data:

```bash
python create_payments.py
```

This creates `payments.csv` and imports it into the database.

### Step 3: Import Data into SQLite

Import all CSV files into the SQLite database:

```bash
python import_to_sqlite.py
```

This will:
- Create `ecom.db` SQLite database
- Create tables with appropriate data types
- Import all CSV data
- Create indexes for better query performance

**Note:** If `ecom.db` already exists, it will be deleted and recreated.

### Step 4: Run Queries

**Customer Order Summary:**
```bash
python customer_order_summary.py
```

This script joins customers, orders, and payments tables to show:
- Total number of orders per customer
- Total amount spent per customer
- Summary statistics (total revenue, average order value, etc.)

**Verify Database:**
```bash
python verify_db.py
```

Shows table row counts and sample queries.

## 📊 Database Schema

### Tables

#### `customers`
- `customer_id` (INTEGER, PRIMARY KEY)
- `first_name` (TEXT)
- `last_name` (TEXT)
- `email` (TEXT)
- `phone` (TEXT)
- `address` (TEXT)
- `city` (TEXT)
- `state` (TEXT)
- `zip_code` (TEXT)
- `country` (TEXT)
- `registration_date` (TEXT)

#### `categories`
- `category_id` (INTEGER, PRIMARY KEY)
- `category_name` (TEXT)
- `description` (TEXT)

#### `products`
- `product_id` (INTEGER, PRIMARY KEY)
- `product_name` (TEXT)
- `description` (TEXT)
- `price` (REAL)
- `category_id` (INTEGER, FOREIGN KEY → categories)
- `stock_quantity` (INTEGER)
- `created_date` (TEXT)

#### `orders`
- `order_id` (INTEGER, PRIMARY KEY)
- `customer_id` (INTEGER, FOREIGN KEY → customers)
- `order_date` (TEXT)
- `status` (TEXT) - Pending, Processing, Shipped, Delivered, Cancelled
- `shipping_address` (TEXT)
- `shipping_city` (TEXT)
- `shipping_state` (TEXT)
- `shipping_zip` (TEXT)
- `total_amount` (REAL)

#### `order_items`
- `order_item_id` (INTEGER, PRIMARY KEY)
- `order_id` (INTEGER, FOREIGN KEY → orders)
- `product_id` (INTEGER, FOREIGN KEY → products)
- `quantity` (INTEGER)
- `unit_price` (REAL)
- `subtotal` (REAL)

#### `payments`
- `payment_id` (INTEGER, PRIMARY KEY)
- `order_id` (INTEGER, FOREIGN KEY → orders)
- `payment_method` (TEXT) - Credit Card, Debit Card, PayPal, Apple Pay, Google Pay, Bank Transfer
- `payment_date` (TEXT)
- `amount` (REAL)
- `payment_status` (TEXT) - Completed, Pending, Failed, Refunded

### Relationships

```
customers (1) ────< (many) orders
orders (1) ────< (many) order_items
orders (1) ────< (many) payments
products (1) ────< (many) order_items
categories (1) ────< (many) products
```

## 📈 Data Statistics

- **Customers**: 500
- **Products**: 200
- **Categories**: 15
- **Orders**: 1,000
- **Order Items**: 3,020
- **Payments**: 1,055

## 🔍 Example SQL Queries

### Top 10 Customers by Spending

```sql
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(p.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN payments p ON o.order_id = p.order_id AND p.payment_status = 'Completed'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;
```

### Most Popular Products

```sql
SELECT 
    p.product_name,
    p.price,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY total_quantity_sold DESC
LIMIT 10;
```

### Revenue by Category

```sql
SELECT 
    cat.category_name,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.subtotal) AS total_revenue
FROM categories cat
JOIN products p ON cat.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_id
ORDER BY total_revenue DESC;
```

### Monthly Sales Trend

```sql
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;
```

## 🛠️ Customization

### Changing Data Volume

Edit `generate_ecommerce_data.py` to modify:
- `NUM_CUSTOMERS` - Number of customers to generate
- `NUM_PRODUCTS` - Number of products
- `NUM_ORDERS` - Number of orders
- `MIN_ORDER_ITEMS` / `MAX_ORDER_ITEMS` - Range of items per order

### Regenerating Data

To regenerate all data from scratch:

```bash
# Delete existing database
rm ecom.db  # On Windows: del ecom.db

# Regenerate CSV files
python generate_ecommerce_data.py

# Create payments
python create_payments.py

# Reimport everything
python import_to_sqlite.py
```

## 📝 Notes

- All data is synthetic and generated using the `Faker` library
- Data is seeded for reproducibility (same data generated each run)
- The database uses SQLite, which is file-based and requires no server setup
- Indexes are automatically created on foreign keys for better query performance

## 🐛 Troubleshooting

### Error: "UNIQUE constraint failed"
- This usually means data already exists. The import script will recreate the database, but if you're running `create_payments.py` separately, it will handle existing data automatically.

### Error: "No module named 'faker'"
- Run `pip install -r requirements.txt` to install dependencies.

### Database file not found
- Make sure you've run `import_to_sqlite.py` first to create the database.

## 📄 License

This project is for educational purposes. The synthetic data generation scripts can be freely used and modified.

## 👤 Author

Created for database and SQL practice purposes.

---

**Happy Querying! 🎉**


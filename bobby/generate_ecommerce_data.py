"""
Generate synthetic e-commerce data for database and SQL practice.
Creates 5 CSV files representing a typical e-commerce database schema.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)

# Configuration
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 200
NUM_CATEGORIES = 15
NUM_ORDERS = 1000
MIN_ORDER_ITEMS = 1
MAX_ORDER_ITEMS = 5

# Generate categories first (needed for products)
categories = []
category_names = [
    "Electronics", "Clothing", "Home & Garden", "Books", "Sports & Outdoors",
    "Toys & Games", "Health & Beauty", "Automotive", "Pet Supplies", "Food & Beverages",
    "Office Supplies", "Musical Instruments", "Baby Products", "Jewelry", "Furniture"
]

print("Generating e-commerce data...")

# 1. Generate categories.csv
print("1. Generating categories.csv...")
with open('categories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['category_id', 'category_name', 'description'])
    
    for i, name in enumerate(category_names, 1):
        description = f"Browse our selection of {name.lower()} products"
        writer.writerow([i, name, description])
        categories.append(i)

# 2. Generate products.csv
print("2. Generating products.csv...")
products = []
product_names = {
    "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch", "Camera", "Speaker", "Monitor"],
    "Clothing": ["T-Shirt", "Jeans", "Dress", "Jacket", "Sneakers", "Hat", "Sweater", "Shorts"],
    "Home & Garden": ["Coffee Maker", "Lamp", "Plant Pot", "Garden Tool", "Cushion", "Curtains", "Rug", "Vase"],
    "Books": ["Novel", "Cookbook", "Biography", "Textbook", "Comic Book", "Dictionary", "Atlas", "Guide"],
    "Sports & Outdoors": ["Basketball", "Tennis Racket", "Yoga Mat", "Dumbbells", "Bicycle", "Tent", "Backpack", "Running Shoes"],
    "Toys & Games": ["Board Game", "Action Figure", "Puzzle", "Building Blocks", "Doll", "RC Car", "Card Game", "Stuffed Animal"],
    "Health & Beauty": ["Shampoo", "Moisturizer", "Perfume", "Toothbrush", "Vitamins", "Face Mask", "Lipstick", "Sunscreen"],
    "Automotive": ["Car Battery", "Tire", "Oil Filter", "Brake Pad", "Car Mat", "Phone Mount", "Dash Cam", "Air Freshener"],
    "Pet Supplies": ["Dog Food", "Cat Litter", "Pet Toy", "Leash", "Pet Bed", "Food Bowl", "Treats", "Collar"],
    "Food & Beverages": ["Coffee", "Tea", "Chocolate", "Snacks", "Juice", "Cereal", "Pasta", "Sauce"],
    "Office Supplies": ["Notebook", "Pen", "Stapler", "Folder", "Desk Organizer", "Calculator", "Printer Paper", "Binder"],
    "Musical Instruments": ["Guitar", "Piano", "Drums", "Violin", "Microphone", "Keyboard", "Ukulele", "Harmonica"],
    "Baby Products": ["Diapers", "Baby Formula", "Pacifier", "Baby Clothes", "Stroller", "Car Seat", "Baby Bottle", "Rattle"],
    "Jewelry": ["Necklace", "Ring", "Earrings", "Bracelet", "Watch", "Brooch", "Anklet", "Pendant"],
    "Furniture": ["Chair", "Table", "Sofa", "Desk", "Bookshelf", "Bed Frame", "Dresser", "Coffee Table"]
}

with open('products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id', 'product_name', 'description', 'price', 'category_id', 'stock_quantity', 'created_date'])
    
    product_id = 1
    for cat_id, cat_name in enumerate(category_names, 1):
        base_names = product_names.get(cat_name, ["Product"])
        for base_name in base_names:
            # Generate multiple variations of each product
            for variant in range(1, 4):
                name = f"{base_name} {variant}" if variant > 1 else base_name
                # Add brand-like prefixes occasionally
                if random.random() < 0.3:
                    brands = ["Premium", "Pro", "Elite", "Classic", "Modern"]
                    name = f"{random.choice(brands)} {name}"
                
                description = f"High-quality {name.lower()} perfect for your needs. Features excellent design and durability."
                price = round(random.uniform(9.99, 999.99), 2)
                stock = random.randint(0, 500)
                created_date = fake.date_between(start_date='-2y', end_date='today')
                
                writer.writerow([product_id, name, description, price, cat_id, stock, created_date])
                products.append(product_id)
                product_id += 1
                if product_id > NUM_PRODUCTS:
                    break
            if product_id > NUM_PRODUCTS:
                break
        if product_id > NUM_PRODUCTS:
            break

# 3. Generate customers.csv
print("3. Generating customers.csv...")
customers = []
with open('customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country', 'registration_date'])
    
    for i in range(1, NUM_CUSTOMERS + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
        phone = fake.phone_number()
        address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
        country = "USA"
        registration_date = fake.date_between(start_date='-3y', end_date='today')
        
        writer.writerow([i, first_name, last_name, email, phone, address, city, state, zip_code, country, registration_date])
        customers.append(i)

# 4. Generate orders.csv
print("4. Generating orders.csv...")
orders = []
order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
start_date = datetime.now() - timedelta(days=365)

with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'customer_id', 'order_date', 'status', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'total_amount'])
    
    for i in range(1, NUM_ORDERS + 1):
        customer_id = random.choice(customers)
        # Order date should be after customer registration
        order_date = fake.date_between(start_date='-1y', end_date='today')
        status = random.choice(order_statuses)
        # Weight statuses towards delivered (more realistic)
        if random.random() < 0.6:
            status = "Delivered"
        elif random.random() < 0.8:
            status = "Shipped"
        
        shipping_address = fake.street_address()
        shipping_city = fake.city()
        shipping_state = fake.state_abbr()
        shipping_zip = fake.zipcode()
        
        # Total amount will be calculated from order items, but we'll set a placeholder
        # It will be updated after generating order_items
        total_amount = 0.0
        
        writer.writerow([i, customer_id, order_date, status, shipping_address, shipping_city, shipping_state, shipping_zip, total_amount])
        orders.append(i)

# 5. Generate order_items.csv and update order totals
print("5. Generating order_items.csv...")
order_totals = {}

with open('order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal'])
    
    order_item_id = 1
    for order_id in orders:
        num_items = random.randint(MIN_ORDER_ITEMS, MAX_ORDER_ITEMS)
        order_total = 0.0
        
        selected_products = random.sample(products, min(num_items, len(products)))
        
        for product_id in selected_products:
            quantity = random.randint(1, 5)
            # Get product price (simplified - in real scenario would query products table)
            # Using a reasonable price range
            unit_price = round(random.uniform(9.99, 299.99), 2)
            subtotal = round(unit_price * quantity, 2)
            order_total += subtotal
            
            writer.writerow([order_item_id, order_id, product_id, quantity, unit_price, subtotal])
            order_item_id += 1
        
        order_totals[order_id] = round(order_total, 2)

# Update orders.csv with correct totals
print("6. Updating orders.csv with totals...")
rows = []
with open('orders.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for row in reader:
        order_id = int(row[0])
        row[8] = order_totals.get(order_id, 0.0)  # Update total_amount
        rows.append(row)

with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("\n✅ Data generation complete!")
print(f"Generated files:")
print(f"  - categories.csv ({NUM_CATEGORIES} categories)")
print(f"  - products.csv ({NUM_PRODUCTS} products)")
print(f"  - customers.csv ({NUM_CUSTOMERS} customers)")
print(f"  - orders.csv ({NUM_ORDERS} orders)")
print(f"  - order_items.csv ({order_item_id - 1} order items)")


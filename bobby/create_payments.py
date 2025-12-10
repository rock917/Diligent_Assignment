"""
Create payments.csv and import it into the database.
Payments table links to orders and includes payment details.
"""

import csv
import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Read orders to create payments for each
orders = []
with open('orders.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        orders.append({
            'order_id': int(row['order_id']),
            'order_date': row['order_date'],
            'total_amount': float(row['total_amount'])
        })

print(f"Creating payments for {len(orders)} orders...")

# Generate payments.csv
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]
payment_statuses = ["Completed", "Completed", "Completed", "Pending", "Failed", "Refunded"]  # Weighted towards Completed

with open('payments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['payment_id', 'order_id', 'payment_method', 'payment_date', 'amount', 'payment_status'])
    
    payment_id = 1
    for order in orders:
        # Most orders have one payment, some might have multiple (partial payments, refunds)
        num_payments = 1 if random.random() < 0.95 else 2
        
        remaining_amount = order['total_amount']
        
        for i in range(num_payments):
            if i == num_payments - 1:
                # Last payment covers remaining amount
                amount = round(remaining_amount, 2)
            else:
                # Partial payment
                amount = round(remaining_amount * random.uniform(0.3, 0.7), 2)
                remaining_amount -= amount
            
            payment_method = random.choice(payment_methods)
            # Payment date is usually same day or within a few days of order
            order_date = datetime.strptime(order['order_date'], '%Y-%m-%d')
            payment_date = order_date + timedelta(days=random.randint(0, 3))
            payment_status = random.choice(payment_statuses)
            
            writer.writerow([
                payment_id,
                order['order_id'],
                payment_method,
                payment_date.strftime('%Y-%m-%d'),
                amount,
                payment_status
            ])
            payment_id += 1

print(f"✓ Created payments.csv with {payment_id - 1} payment records")

# Import into database
print("Importing payments into database...")
conn = sqlite3.connect('ecom.db')
cursor = conn.cursor()

# Create payments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        payment_method TEXT,
        payment_date TEXT,
        amount REAL,
        payment_status TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
''')

# Delete existing data if table already has records
cursor.execute("SELECT COUNT(*) FROM payments")
existing_count = cursor.fetchone()[0]
if existing_count > 0:
    print(f"  Found {existing_count} existing payment records. Deleting...")
    cursor.execute("DELETE FROM payments")
    conn.commit()

# Import data
with open('payments.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO payments (payment_id, order_id, payment_method, payment_date, amount, payment_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            int(row['payment_id']),
            int(row['order_id']),
            row['payment_method'],
            row['payment_date'],
            float(row['amount']),
            row['payment_status']
        ))

conn.commit()
cursor.execute("SELECT COUNT(*) FROM payments")
count = cursor.fetchone()[0]
print(f"✓ Imported {count} payments into database")
conn.close()

print("✅ Payments table created successfully!")


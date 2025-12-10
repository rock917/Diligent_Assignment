"""Quick verification script to check the database structure."""
import sqlite3

conn = sqlite3.connect('ecom.db')
cursor = conn.cursor()

print("Database Tables and Row Counts:")
print("=" * 50)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"{table_name:20} {count:>6} rows")

print("\n" + "=" * 50)
print("\nSample query - Top 5 customers by order count:")
print("-" * 50)
cursor.execute("""
    SELECT c.customer_id, c.first_name, c.last_name, COUNT(o.order_id) as order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    ORDER BY order_count DESC
    LIMIT 5
""")
results = cursor.fetchall()
for row in results:
    print(f"Customer {row[0]}: {row[1]} {row[2]} - {row[3]} orders")

conn.close()


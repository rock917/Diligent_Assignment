"""
Import CSV files into SQLite database for e-commerce data.
Creates ecom.db and imports all CSV files as tables.
"""

import csv
import sqlite3
import os
from pathlib import Path

# Database file name
DB_NAME = 'ecom.db'

# CSV files to import (in order of dependencies)
CSV_FILES = [
    ('categories.csv', 'categories'),
    ('customers.csv', 'customers'),
    ('products.csv', 'products'),
    ('orders.csv', 'orders'),
    ('order_items.csv', 'order_items'),
    ('payments.csv', 'payments'),  # Optional - will skip if doesn't exist
]

def get_csv_headers(csv_file):
    """Read the first line of CSV to get column headers."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
    return headers

def infer_sqlite_type(value):
    """Infer SQLite data type from a sample value."""
    if value is None or value == '':
        return 'TEXT'
    
    # Try to convert to integer
    try:
        int(value)
        return 'INTEGER'
    except ValueError:
        pass
    
    # Try to convert to float
    try:
        float(value)
        return 'REAL'
    except ValueError:
        pass
    
    # Default to TEXT
    return 'TEXT'

def get_column_types(csv_file, num_samples=10):
    """Determine column types by sampling rows."""
    headers = get_csv_headers(csv_file)
    types = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        samples = []
        for i, row in enumerate(reader):
            if i >= num_samples:
                break
            samples.append(row)
    
    for header in headers:
        sample_values = [row[header] for row in samples if header in row and row[header]]
        if sample_values:
            types[header] = infer_sqlite_type(sample_values[0])
        else:
            types[header] = 'TEXT'
    
    return types

def create_table(conn, table_name, csv_file):
    """Create a table based on CSV file structure."""
    headers = get_csv_headers(csv_file)
    types = get_column_types(csv_file)
    
    # Create column definitions
    columns = []
    for header in headers:
        sql_type = types.get(header, 'TEXT')
        # Clean header name for SQL (replace spaces, special chars)
        clean_header = header.replace(' ', '_').replace('-', '_').lower()
        columns.append(f'"{clean_header}" {sql_type}')
    
    # Create table SQL
    create_sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(columns)}
    )
    '''
    
    conn.execute(create_sql)
    conn.commit()
    print(f"  ✓ Created table: {table_name}")

def import_csv_data(conn, table_name, csv_file):
    """Import data from CSV file into SQLite table."""
    headers = get_csv_headers(csv_file)
    clean_headers = [h.replace(' ', '_').replace('-', '_').lower() for h in headers]
    
    # Count rows first
    with open(csv_file, 'r', encoding='utf-8') as f:
        row_count = sum(1 for line in f) - 1  # Subtract header
    
    # Prepare insert statement
    placeholders = ','.join(['?' for _ in headers])
    quoted_headers = ','.join([f'"{h}"' for h in clean_headers])
    insert_sql = f'INSERT INTO {table_name} ({quoted_headers}) VALUES ({placeholders})'
    
    # Read and insert data
    inserted = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        batch = []
        for row in reader:
            # Ensure row has same length as headers (pad with None if needed)
            while len(row) < len(headers):
                row.append(None)
            batch.append(row[:len(headers)])
            
            # Insert in batches of 1000
            if len(batch) >= 1000:
                conn.executemany(insert_sql, batch)
                inserted += len(batch)
                batch = []
        
        # Insert remaining rows
        if batch:
            conn.executemany(insert_sql, batch)
            inserted += len(batch)
    
    conn.commit()
    print(f"  ✓ Imported {inserted} rows into {table_name}")

def create_indexes(conn):
    """Create useful indexes for common queries."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);",
        "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);",
        "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);",
        "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);",
        "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);",
    ]
    
    for index_sql in indexes:
        try:
            conn.execute(index_sql)
        except sqlite3.OperationalError as e:
            print(f"  ⚠ Could not create index: {e}")
    
    conn.commit()
    print("  ✓ Created indexes")

def main():
    """Main function to import all CSV files into SQLite."""
    print("=" * 60)
    print("Importing CSV files into SQLite database: ecom.db")
    print("=" * 60)
    
    # Remove existing database if it exists
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Removed existing {DB_NAME}")
    
    # Create database connection
    conn = sqlite3.connect(DB_NAME)
    print(f"\nCreated database: {DB_NAME}\n")
    
    # Import each CSV file
    imported_count = 0
    skipped_count = 0
    
    for csv_file, table_name in CSV_FILES:
        if not os.path.exists(csv_file):
            print(f"⚠ Skipping {csv_file} (file not found)")
            skipped_count += 1
            continue
        
        print(f"Processing {csv_file}...")
        try:
            create_table(conn, table_name, csv_file)
            import_csv_data(conn, table_name, csv_file)
            imported_count += 1
            print()
        except Exception as e:
            print(f"  ✗ Error importing {csv_file}: {e}\n")
            skipped_count += 1
    
    # Create indexes
    print("Creating indexes...")
    create_indexes(conn)
    print()
    
    # Print summary
    print("=" * 60)
    print("Import Summary:")
    print(f"  ✓ Successfully imported: {imported_count} tables")
    if skipped_count > 0:
        print(f"  ⚠ Skipped: {skipped_count} files")
    print(f"  📁 Database: {DB_NAME}")
    print("=" * 60)
    
    # Show table info
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\nTables in database:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} rows")
    
    conn.close()
    print("\n✅ Import complete!")

if __name__ == '__main__':
    main()


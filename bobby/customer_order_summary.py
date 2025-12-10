"""
Query script that connects to SQLite database ecom.db,
runs an SQL query joining customers, orders, and payments tables,
and prints the total number of orders and total amount spent by each customer.
"""

import sqlite3

def main():
    # Connect to the database
    conn = sqlite3.connect('ecom.db')
    cursor = conn.cursor()
    
    # SQL query joining customers, orders, and payments
    # We'll aggregate payments by order, then by customer
    query = """
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.email,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COALESCE(SUM(p.amount), 0) AS total_amount_spent
    FROM 
        customers c
    LEFT JOIN 
        orders o ON c.customer_id = o.customer_id
    LEFT JOIN 
        payments p ON o.order_id = p.order_id AND p.payment_status = 'Completed'
    GROUP BY 
        c.customer_id, c.first_name, c.last_name, c.email
    ORDER BY 
        total_amount_spent DESC, total_orders DESC
    """
    
    print("=" * 100)
    print("Customer Order Summary")
    print("Total number of orders and total amount spent by each customer")
    print("=" * 100)
    print()
    
    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Prepare data for display
    headers = ["Customer ID", "Customer Name", "Email", "Total Orders", "Total Amount Spent ($)"]
    table_data = []
    
    for row in results:
        customer_id, customer_name, email, total_orders, total_amount = row
        table_data.append([
            customer_id,
            customer_name,
            email,
            total_orders,
            f"${total_amount:,.2f}"
        ])
    
    # Display results in a formatted table
    # Print header
    print(f"{'Customer ID':<12} {'Customer Name':<25} {'Email':<30} {'Orders':<8} {'Total Spent':<15}")
    print("-" * 100)
    
    # Print data rows
    for row in table_data:
        customer_id, customer_name, email, total_orders, total_amount = row
        # Truncate email if too long
        email_display = email[:27] + "..." if len(email) > 30 else email
        customer_name_display = customer_name[:22] + "..." if len(customer_name) > 25 else customer_name
        print(f"{customer_id:<12} {customer_name_display:<25} {email_display:<30} {total_orders:<8} {total_amount:<15}")
    
    # Print summary statistics
    print()
    print("=" * 100)
    print("Summary Statistics:")
    print("-" * 100)
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT customer_id) as customers_with_orders,
            SUM(total_orders) as total_all_orders,
            SUM(total_amount_spent) as total_all_revenue
        FROM (
            SELECT 
                c.customer_id,
                COUNT(DISTINCT o.order_id) AS total_orders,
                COALESCE(SUM(p.amount), 0) AS total_amount_spent
            FROM 
                customers c
            LEFT JOIN 
                orders o ON c.customer_id = o.customer_id
            LEFT JOIN 
                payments p ON o.order_id = p.order_id AND p.payment_status = 'Completed'
            GROUP BY 
                c.customer_id
        )
    """)
    stats = cursor.fetchone()
    customers_with_orders, total_all_orders, total_all_revenue = stats
    
    print(f"Total Customers: {total_customers}")
    print(f"Customers with Orders: {customers_with_orders}")
    print(f"Total Orders: {total_all_orders}")
    print(f"Total Revenue: ${total_all_revenue:,.2f}")
    print(f"Average Order Value: ${total_all_revenue / total_all_orders:,.2f}" if total_all_orders > 0 else "Average Order Value: $0.00")
    print("=" * 100)
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()


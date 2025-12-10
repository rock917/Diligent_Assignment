├── generate_ecommerce_data.py      # Creates categories, products, customers, orders, order_items CSVs
├── create_payments.py              # Creates payments.csv and imports it into database
├── import_to_sqlite.py             # Builds ecom.db and imports all CSV data
├── customer_order_summary.py       # SQL analytics (orders + total spend per customer)
├── verify_db.py                    # Quick DB verification and sample queries
│
├── categories.csv
├── products.csv
├── customers.csv
├── orders.csv
├── order_items.csv
├── payments.csv
│
├── ecom.db                         # Auto-generated SQLite database
├── requirements.txt                # Dependencies (Faker)
└── prompt.txt                      # Instructions used to create the project

# Project by Harsha Vardhan Reddy

# E-commerce Synthetic Data Project

This repository contains a small sample e-commerce dataset (CSV files), a Python ingestion script that loads the CSVs into a SQLite database (`ecom.db`), and example SQL queries.

## Files
- `users.csv` - sample users
- `products.csv` - sample products
- `orders.csv` - sample orders
- `order_items.csv` - order line items
- `payments.csv` - payments table
- `ingest_csvs_to_sqlite.py` - Python script to create `ecom.db` from the CSVs
- `ecom.db` - pre-built SQLite database (optional; included for convenience)
- `README.md` - this file

## How to run locally

1. Clone the repo:
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

2. (Optional) Create a virtual environment and install dependencies (none required — uses Python stdlib):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Run the ingestion script:
```bash
python ingest_csvs_to_sqlite.py
```

This will create `ecom.db` in the project folder.

## Example SQL queries

1. Total sales per user (exclude refunded orders)
```sql
SELECT
  u.user_id,
  u.first_name || ' ' || u.last_name AS customer_name,
  COUNT(DISTINCT o.order_id) AS orders_count,
  ROUND(SUM(p.paid_amount), 2) AS total_paid
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN payments p ON p.order_id = o.order_id
WHERE o.status != 'refunded'
GROUP BY u.user_id
ORDER BY total_paid DESC;
```

2. Product-wise revenue and units sold
```sql
SELECT
  pr.product_id,
  pr.name,
  SUM(oi.quantity) AS units_sold,
  ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM products pr
JOIN order_items oi ON oi.product_id = pr.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status != 'refunded'
GROUP BY pr.product_id
ORDER BY revenue DESC;
```

## License
Harshavardhanreddy


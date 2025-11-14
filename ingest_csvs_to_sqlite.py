# Author: Harsha Vardhan Reddy
import sqlite3
import csv
from pathlib import Path

BASE = Path(__file__).parent
DB_PATH = BASE / "ecom.db"

def create_tables(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        signup_date TEXT,
        country TEXT
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        sku TEXT,
        name TEXT,
        category TEXT,
        price REAL
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        order_date TEXT,
        status TEXT,
        total_amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        paid_amount REAL,
        payment_method TEXT,
        paid_at TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );""")
    conn.commit()

def insert_from_csv(conn, table, csv_path):
    cur = conn.cursor()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        placeholders = ",".join(["?"] * len(headers))
        query = f"INSERT OR REPLACE INTO {table} ({','.join(headers)}) VALUES ({placeholders})"
        rows = [tuple(r) for r in reader]
        cur.executemany(query, rows)
    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    insert_from_csv(conn, "users", BASE / "users.csv")
    insert_from_csv(conn, "products", BASE / "products.csv")
    insert_from_csv(conn, "orders", BASE / "orders.csv")
    insert_from_csv(conn, "order_items", BASE / "order_items.csv")
    insert_from_csv(conn, "payments", BASE / "payments.csv")
    conn.close()
    print(f"SQLite database created at: {DB_PATH}")

if __name__ == "__main__":
    main()

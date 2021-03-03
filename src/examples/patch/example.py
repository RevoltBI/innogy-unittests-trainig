import pandas as pd
import sqlite3
import os

def store_contractors(since, conn):
    contractors = pd.read_sql_query(
        "SELECT c.contractor_id, name, invoice_id, amount, maturity_date FROM contractors c LEFT JOIN invoices i ON c.contractor_id=i.contractor_id", conn)
    contractors.to_sql(f"conntractors_stats_{since.strftime('%Y-%m-%d')}", conn, if_exists="replace")
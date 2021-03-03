import pandas as pd


def load_data():
    return pd.read_sql_query("SELECT c.contractor_id, name, invoice_id, amount, maturity_date FROM contractors c LEFT JOIN invoices i ON c.contractor_id=i.contractor_id", conn)


def get_contracts(since):
    contractors = load_data()
    return contractors[contractors['maturity_date'] >= since]
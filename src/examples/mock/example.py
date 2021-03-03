import pandas as pd
import sqlite3
import os


def store_df(since, contractors:pd.DataFrame, conn):     
    if since is None:
        raise ValueError("Since must not be empty")
    
    new_table_name = f"conntractors_stats_{since.strftime('%Y_%m_%d')}"
    contractors.to_sql(new_table_name, conn, if_exists="replace")
    
    return new_table_name
    

def store_single_date(single_day, date, conn):
    new_table_name = f"contractors_{date}"
    single_day.to_sql(new_table_name, conn, if_exists="replace")

    
def store_df_per_date(contractors:pd.DataFrame, store_function):
    result = []
    for date in contractors.maturity_date.unique():
        result.append(store_function(contractors[contractors["maturity_date"] == date]))
        
    return result
        
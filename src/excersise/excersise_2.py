"""
1. Test prepare dates method and confirm result by a code coverage
2. Prepare a test of fetch_log_dataframes method
"""
import re
import mysql.connector
import matplotlib 
import pandas as pd

def get_connection(host, username, password):
    if not host or not username or not password:
        raise ValueError("Incomplete credentials")
    
    return mysql.connector.connect(host=host,user=username,password=password) 

def prepare_dates(dates):
    if dates is None:
        raise ValueError("Dates must not be empty")
        
    if not isinstance(dates, list) and not isinstance(dates, str):
        raise ValueError("Dates must be either a list of dates or list of strings")
        
    if isinstance(dates, str):
        dates = [dates]
        
    return dates

def fetch_log_dataframes(dates, conn):
    frames = []
    for date in dates:
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date) is None:
            raise ValueError(f"Date {date} does not have a valid format YYYY-MM-DD")
        
    
        
        frame = pd.read_sql_query( 
            f"SELECT timestamp, message, severity, line_no, file FROM log_daily_{date.replace('-', '_')}", conn) # Table name example log_daily_2
        
        frames.append(frame)
        
    return frames

def plot_log_stats(frame):
    grouped = merged[["severity", "file", "message"]].groupby(["severity", "log_line"]).agg(["count"])
    
    grouped.unstack("severity").plot.bar(stacked=True)

    
def prepare_print_daily_logs_statistics(dates, host, username, password):
    """
    The function loads logs from tables that store daily logs. The logs are then merged and the function counts log types per file during the day
    and prints a bar chart that represents count of different log severities as a stacked barchart.
    
    :param dates: list of dates or a single date
    :param host: database host name
    :param username: database username
    :param password: string
    """
    dates = prepare_dates(dates)    
    conn = get_connection(host, username, password)    
    frames = fetch_log_dataframes(dates, conn)        
    plot_data(pd.concat(frames))
    
    
    
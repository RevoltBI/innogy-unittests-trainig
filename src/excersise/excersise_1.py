"""
Refactor method in such way that is easy to unit test and implement adequate unit test. 
"""
import datetime
import re
import tempfile
import os
from ftplib import FTP

import mysql.connector
import pandas as pd

from .stats_counter import Stats

FTP_USERNAME = "test"
FTP_PASSWORD = "ninja"
FTP_HOST = "ftp.host.com"

def prepare_print_daily_logs_statistics(dates, host, username, password):
    """
    The function loads logs from tables that store daily logs. The logs are then merged and the function counts log types per file during the day
    and prints a bar chart that represents count of different log severities as a stacked barchart.
    
    :param dates: list of dates or a single date
    :param host: database host name
    :param username: database username
    :param password: string
    """
    if dates is None and validate_date_format(dates):
        raise ValueError("Dates must not be empty")
        
    if not isinstance(dates, list) and not isinstance(dates, str):
        raise ValueError("Dates must be either a list of dates or list of strings")
        
    if isinstance(dates, str):
        dates = [dates]
    
    frames = []
    
    if not host or not username or not password:
        raise ValueError("Incomplete credentials")
    
    conn = mysql.connector.connect(
          host=host,
          user=username,
          password=password
        ) 
    
    for date in dates:
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date) is None:
            raise ValueError(f"Date {date} does not have a valid format YYYY-MM-DD")
        
    
        
        frame = pd.read_sql_query( 
            f"SELECT timestamp, message, severity, line_no, file FROM log_daily_{date.replace('-', '_')}", conn) # Table name example log_daily_2
        Stats().process(frame)
        frames.append(frame)
        
    
    merged = pd.concat(frames)
    
    grouped = merged[["severity", "file", "message"]].groupby(["severity", "log_line"]).agg(["count"])
    
    grouped.unstack("severity").plot.bar(stacked=True)
    
    ftp = FTP(FTP_HOST)
    ftp.login(FTP_USERNAME, FTP_PASSWORD)
    tmp_file = tempfile.mktemp()
    try:
        merged.to_csv(tmp_file)
        with open(tmp_file, "r") as fp:
            ftp.storbinary(f"STOR log_run_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv", fp)
    finally:
        os.remove(tmp_file)
        ftp.quit()

    
"""
1. Test prepare_dates method and confirm result by a code coverage
2. Prepare a test of fetch_log_dataframes method
3. Prepare a test for plot_log_stats
4. Prepare a test for send_to_ftp
5. Test dependency.Stats.PandasInstance
6. Test dependency.Stats.PandasInstance
7. Test prepare_print_daily_logs_statistics
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


def get_connection(host, username, password):
    if not host or not username or not password:
        raise ValueError("Incomplete credentials")

    return mysql.connector.connect(host=host, user=username, password=password)


def prepare_dates(dates):
    if dates is None:
        raise ValueError("Dates must not be empty")

    if not isinstance(dates, list) and not isinstance(dates, str):
        raise ValueError("Dates must be either a list of dates or list of strings")

    if isinstance(dates, str):
        dates = [dates]
        
        

    return dates


def fetch_log_dataframes(dates, conn, stats_callback):
    frames = []
    for date in dates:
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date) is None:
            raise ValueError(f"Date {date} does not have a valid format YYYY-MM-DD")

        frame = pd.read_sql_query(
            f"SELECT timestamp, message, severity, line_no, file FROM log_daily_{date.replace('-', '_')}",
            conn)  # Table name example log_daily_2

        stats_callback(frame)
        frames.append(frame)

    return frames


def plot_log_stats(frame):
    grouped = frame[["severity", "file", "message"]].groupby(["severity", "log_line"]).agg(["count"])
    grouped.unstack("severity").plot.bar(stacked=True)


def send_to_ftp(frames):
    """
    Stores taken result set to CSV file and sends the file to FPT
    """
    if frames:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        tmp_file = tempfile.mktemp()
        try:
            frames.to_csv(tmp_file)
            with open(tmp_file, "r") as fp:
                ftp.storbinary(f"STOR log_run_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv", fp)
        finally:
            os.remove(tmp_file)
            ftp.quit()


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
    frames = fetch_log_dataframes(dates, conn, Stats().process)
    frames_concatenated = pd.concat(frames)
    plot_data(frames_concatenated)

    send_to_ftp(frames_concatenated)

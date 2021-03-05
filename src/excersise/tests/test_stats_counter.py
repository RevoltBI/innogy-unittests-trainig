import pandas as pd
from pytest import fixture

from ..stats_counter import Stats


@fixture(autouse=True)
def reset_stats():
    stats = Stats()
    stats._Stats__call_count = 0
    stats._Stats__total_rows_processed = 0
    stats._Stats__processed = set()
    stats._Stats__average_rows_count = 0


def test_process_empty():
    stats = Stats()

    stats.process(None)

    assert str(stats) == "[Total count: 0, Total rows processed: 0, Average row count: 0"


def test_process_two_different():
    stats = Stats()

    df1 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })

    df2 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, ],
        "name": ["Other", "Other", "Other", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01"],
        "amount": [100, 200, 300, 200, 300]
    })

    stats.process(df1)
    stats.process(df2)

    assert str(stats) == "[Total count: 2, Total rows processed: 11, Average row count: 5.5"


def test_process_two_the_same():
    stats = Stats()

    df1 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })

    df2 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })

    df3 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2],
        "name": ["Other", "Other", "Other", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01"],
        "amount": [100, 200, 300, 200]
    })

    stats.process(df1)
    stats.process(df2)
    stats.process(df3)

    assert str(stats) == "[Total count: 2, Total rows processed: 10, Average row count: 5.0"

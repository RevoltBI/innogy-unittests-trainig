from ..stats_counter import Stats
from unittest.mock import MagicMock, patch, call, ANY
from pytest import fixture
import pandas as pd

@fixture
def reset_stats():
    stats = Stats()
    stats._Stats__call_count = 0
    stats._Stats__total_rows_processed = 0
    stats._Stats__processed = set()
    stats._Stats__average_rows_count = 0


def test_process_empty_input():
    stats = Stats()
    
    assert not stats.process(None), "The process result should be False"
    
def _init_df():
    return (pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    }))
    
def test_process_add_one():
    df1, df2 = _init_df()
    
    stats = Stats()
    
    result = stats.process(df)
    assert result, "The process result should return True after uniquie DF"
    
    assert stats._Stats__call_count == 1
    assert stats._Stats__total_rows_processed == 6
    assert stats._Stats__average_rows_count == 6
    
    assert len(stats._Stats__processed) == 1

def test_process_add_two_the_same(reset_stats):
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
    
    stats = Stats()
    
    assert stats.process(df1)    
    result = stats.process(df2)
    assert not result, "The process result of DF that was already processed should return False"
    
    assert stats._Stats__call_count == 1
    assert stats._Stats__total_rows_processed == 6
    assert stats._Stats__average_rows_count == 6
    
    assert len(stats._Stats__processed) == 1
    
def test_process_add_two_different(reset_stats):
    df1 = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 4],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })
    
    df2 = pd.DataFrame({
        "contractor_id": [1, 1, 2, 2, 3],
        "name": ["David", "David", "Maria", "Maria", "Eva"],
        "maturity_date": ["2020-02-01", "2020-03-01", "2020-01-01", "2020-02-01", "2020-03-01"],
        "amount": [200, 300, 200, 300, 400]
    })
    
    stats = Stats()
    
    stats.process(df1)    
    result = stats.process(df2)
    assert result,  "The process result should return True after uniquie DF"
    
    assert stats._Stats__call_count == 2
    assert stats._Stats__total_rows_processed == 11
    assert stats._Stats__average_rows_count == 5.5
    
    assert len(stats._Stats__processed) == 2
from .. import example as e
from unittest.mock import MagicMock, call, ANY
import pytest
import datetime
import pandas as pd

def test_store_df_empty_value():
    df_contractor_mock = MagicMock()
    conn_mock = MagicMock()
    
    with pytest.raises(ValueError) as excinfo:
        e.store_df(None, df_contractor_mock, conn_mock)
    
    
    assert str(excinfo.value) == "Since must not be empty"
    
    
def test_store_df_correct():
    df_contractor_mock = MagicMock()
    conn_mock = MagicMock()
    
    expected_new_table_name = "conntractors_stats_2020_01_01"
    
    new_table_name = e.store_df(datetime.datetime.strptime("2020-01-01", "%Y-%m-%d"), df_contractor_mock, conn_mock)
    
    
    assert new_table_name == expected_new_table_name
    df_contractor_mock.to_sql(expected_new_table_name, conn_mock, if_exists="replace")
    
    
def test_store_df_per_date():
    df = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01","2020-03-01", "2020-01-01", "2020-02-01","2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })
    
    store_function = MagicMock(side_effect=[True, False, True])
    
    assert e.store_df_per_date(df, store_function) == [True, False, True]
    
def test_store_df_per_date_exception_thrown():
    df = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01","2020-03-01", "2020-01-01", "2020-02-01","2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })
    
    store_function = MagicMock(side_effect=ValueError("Test error"))
    
    with pytest.raises(ValueError):
        e.store_df_per_date(df, store_function)
    
    
def test_store_df_per_date_exception_thrown_second_call():
    df = pd.DataFrame({
        "contractor_id": [1, 1, 1, 2, 2, 2],
        "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
        "maturity_date": ["2020-01-01", "2020-02-01","2020-03-01", "2020-01-01", "2020-02-01","2020-03-01"],
        "amount": [100, 200, 300, 200, 300, 400]
    })
    
    
    counter = 0
    def side_effect(*args):
        nonlocal counter
        if counter < 1:
            counter += 1
        else:
            raise ValueError("Test Message")

        
    
    store_function = MagicMock(side_effect=side_effect)
    
    with pytest.raises(ValueError):
        e.store_df_per_date(df, store_function)
        
    store_function.assert_has_calls([call(ANY), call(ANY)])
    
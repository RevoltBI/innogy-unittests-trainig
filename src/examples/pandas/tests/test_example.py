from .. import example as e
from unittest.mock import patch
import pandas as pd
import numpy as np

@patch("examples.pandas.example.load_data", return_value=pd.DataFrame({
    "contractor_id": [1, 1, 1, 2, 2, 2],
    "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
    "maturity_date": ["2020-01-01", "2020-02-01","2020-03-01", "2020-01-01", "2020-02-01","2020-03-01"],
    "amount": [100, 200, 300, 200, 300, 400]
}))
def test_get_contracts(load_data_mock):
    pd.testing.assert_frame_equal(
        pd.DataFrame({
            "contractor_id": [1, 2],
            "name": ["David", "Maria"],
            "maturity_date": ["2020-03-01", "2020-03-01"],
            "amount": [300, 400]
        }),
        e.get_contracts("2020-03-01").reset_index(drop=True) # This is because even indices has to be equal in order to have 2 DF equal
    )
    

@patch("examples.pandas.example.load_data", return_value=pd.DataFrame({
    "contractor_id": [1, 1, 1, 2, 2, 2],
    "name": ["David", "David", "David", "Maria", "Maria", "Maria"],
    "maturity_date": ["2020-01-01", "2020-02-01","2020-03-01", "2020-01-01", "2020-02-01","2020-03-01"],
    "amount": [100, 200, 300, 200, 300, 400]
}))
def test_get_weaker_test(load_data_mock):
    assert np.array_equal(
        pd.DataFrame({
            "contractor_id": [1, 2],
            "name": ["David", "Maria"],
            "maturity_date": ["2020-03-01", "2020-03-01"],
            "amount": [300, 400]
        }).values,
        e.get_contracts("2020-03-01").values # Weaker check for arrays only
    )
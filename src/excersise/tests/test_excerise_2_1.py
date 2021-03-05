import pytest
from .. import excersise_2 as e

def test_prepare_dates_dates_missing():
    with pytest.raises(ValueError) as exc_info:
        e.prepare_dates(None)
        
    assert "Dates must not be empty" == str(exc_info.value)
        

def test_prepare_dates_dates_not_valid_types():
    with pytest.raises(ValueError) as exc_info:
        e.prepare_dates(1)
        
    assert "Dates must be either a list of dates or list of strings" == str(exc_info.value)
        
def test_prepare_dates_date_a_string():
    assert ["2020-01-01"] == e.prepare_dates("2020-01-01")

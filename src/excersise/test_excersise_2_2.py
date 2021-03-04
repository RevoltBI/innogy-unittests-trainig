import pytest
from . import excersise_2 as e
from unittest.mock import MagicMock, patch, call


def test_fetch_log_dataframes_invalid_date_format():
    conn_mock = MagicMock()
    with pytest.raises(ValueError) as exc_info:
        e.fetch_log_dataframes(["2020-01-ZZ"], conn_mock)
        
    assert "Date 2020-01-ZZ does not have a valid format YYYY-MM-DD" == str(exc_info.value)


@patch(__package__ + ".excersise_2.pd")
def test_fetch_log_dataframes_2_files(pd_mock):
    result1 = MagicMock()
    result2 = MagicMock()
    pd_mock.read_sql_query = MagicMock(side_effect=[result1, result2])
    conn_mock = MagicMock()
    
    assert [result1, result2] == e.fetch_log_dataframes(["2020-01-01", "2020-01-02"], conn=conn_mock)
    pd_mock.read_sql_query.assert_has_calls([
        call("SELECT timestamp, message, severity, line_no, file FROM log_daily_2020_01_01", conn_mock),
        call("SELECT timestamp, message, severity, line_no, file FROM log_daily_2020_01_02", conn_mock)
    ])
    
from .. import example as e
from unittest.mock import MagicMock, patch, ANY
import datetime

@patch("examples.patch.example.pd")
def test_store_contractors(pd_mock):
    contractors_mock = MagicMock()
    pd_mock.read_sql_query = MagicMock(return_value=contractors_mock)
    connection_mock = MagicMock()
    
    e.store_contractors(datetime.datetime.strptime("2020-01-01", "%Y-%m-%d"), connection_mock)
    pd_mock.read_sql_query.assert_called_once_with(ANY, connection_mock)
    contractors_mock.to_sql.assert_called_once_with("conntractors_stats_2020-01-01", connection_mock, if_exists="replace")
    
    
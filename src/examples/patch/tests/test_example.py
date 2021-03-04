from .. import example as e
from unittest.mock import MagicMock, patch, ANY
import datetime

@patch("examples.patch.example.pd.read_sql_query")
def test_store_contractors(read_sql_query_mock):
    contractors_mock = MagicMock()
    read_sql_query_mock.return_value=contractors_mock
    connection_mock = MagicMock()
    
    e.store_contractors(datetime.datetime.strptime("2020-01-01", "%Y-%m-%d"), connection_mock)
    read_sql_query_mock.assert_called_once_with(ANY, connection_mock)
    
    contractors_mock.to_sql.assert_called_once_with("conntractors_stats_2020-01-01", connection_mock, if_exists="replace")
    
    
from ..excersise_3 import get_col_binner


def test_get_col_binner_midle():
    binner = get_col_binner([100, 1000, 10000])

    assert "100-1000" == binner(200)


def test_get_col_binner_lower():
    binner = get_col_binner([100, 1000, 10000])

    assert binner(20) == "<100"


def test_get_col_binner_upper():
    binner = get_col_binner([100, 1000, 10000])

    assert binner(100000) == "10000≤"

from . import example as e

def test_add_number_if_odd():
    assert e.add_number_if_odd(1, 2) == 1
    assert e.add_number_if_odd(1, 0) == 1
    assert e.add_number_if_odd(1, 3) == 4
    
def test_add_number_if_odd_none_input():
    assert e.add_number_if_odd(None, 1) == 1
    assert e.add_number_if_odd(1, None) == 1

def add_number_if_odd(base, number):
    adj_base = 0 if base is None else base
    return adj_base + (0 if number is None or number % 2 == 0 else number)
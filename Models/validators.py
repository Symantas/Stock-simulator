def is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0

def is_non_negative_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0

def is_number_in_range(value, lo, hi):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and lo <= value <= hi

def is_non_empty_string(value):
    return isinstance(value, str) and len(value) > 0

def is_non_negative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0

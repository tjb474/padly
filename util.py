from datetime import datetime

def to_int(value, default=0):
    """Convert a string to an integer, with a default for empty/invalid strings."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def to_float(value, default=0.0):
    """Convert a string to a float, with a default for empty/invalid strings."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def format_date(date_str, from_format="%Y-%m-%d", to_format="%d-%m-%Y", default=None):
    """Convert a date string from one format to another, handling empty/invalid strings."""
    try:
        return datetime.strptime(date_str, from_format).strftime(to_format)
    except (ValueError, TypeError):
        return default

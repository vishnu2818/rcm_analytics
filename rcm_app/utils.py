from decimal import Decimal, InvalidOperation
import pandas as pd
from datetime import datetime


def parse_decimal(value):
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0.00')


def parse_date(val):
    try:
        if pd.isna(val):
            return datetime(2000, 1, 1).date()
        if isinstance(val, datetime):
            return val.date()
        return pd.to_datetime(val).date()
    except Exception:
        return datetime(2000, 1, 1).date()


def convert_to_serializable(val):
    if pd.isna(val):
        return None
    return str(val).strip() if isinstance(val, str) else val

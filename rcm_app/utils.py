from decimal import Decimal, InvalidOperation
import re
import numpy as np
import pandas as pd
from datetime import datetime





from datetime import datetime, date
import pandas as pd
from datetime import datetime, date

def parse_date(value):
    if pd.isnull(value) or value == '':
        return None
    if isinstance(value, date):
        return value  # Already a date or datetime
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime().date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, float) or isinstance(value, int):  # Excel serial format
        try:
            return pd.to_datetime(value, unit='D', origin='1899-12-30').date()
        except Exception as e:
            print(f"⚠️ Cannot parse float date: {value} - {e}")
            return None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    print(f"⚠️ Unknown date format: {value} ({type(value)})")
    return None



def safe_date(value):
    if isinstance(value, datetime):
        return value.date()
    elif isinstance(value, str):
        return parse_date(value)
    return None

def parse_decimal(val):
    try:
        if pd.isna(val) or val == '':
            return Decimal('0.00')
        return Decimal(str(val))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0.00')


def classify_claim_status(row, payment_status, ar_status):
    """
    Determine claim status based on the 12-step logic provided
    Returns tuple: (claim_status, debug_steps)
    """
    debug_steps = []

    #  Extract relevant fields using model field access
    balance = float(row.balance_due or 0)
    charge = float(row.net_charges or 0)
    payments = float(row.payments or 0)
    status = (row.status or '').lower()
    payor = (row.cur_pay_category or '').lower()
    pri_payor = (row.pri_payor_category or '').lower()
    schedule_track = (row.schedule_track or '').lower()

    # Rest of the function remains the same...
    # Step 1: Negative balance
    if balance < 0:
        debug_steps.append("Step 1: Negative balance detected")
        return "Negative balance", debug_steps

    # Step 2: Canceled but closed
    if (payment_status == "Canceled Trip" and status == 'closed') or \
            (balance == 0 and charge == 0 and status == 'closed'):
        debug_steps.append("Step 2: Canceled with closed status")
        return "Canceled but Status Closed", debug_steps

    # Step 3: Canceled with Posting
    if payment_status == "Canceled Trip" and \
            (balance != 0 or charge != 0 or payments != 0):
        debug_steps.append("Step 3: Canceled with financial activity")
        return "Canceled with Posting", debug_steps

    # Step 4: Canceled Trip
    if balance == 0 and charge == 0 and status == 'canceled':
        debug_steps.append("Step 4: Canceled trip with no activity")
        return "Canceled Trip", debug_steps

    # Step 5: New Trips
    if status == 'new' or 'emsmart processed' in schedule_track:
        debug_steps.append("Step 5: New trip detected")
        return "New Trips", debug_steps

    # Step 6: Paid & Closed
    if payment_status == "Paid & Closed" or \
            (balance == 0 and charge > 0 and payments > 0):
        debug_steps.append("Step 6: Paid and closed claim")
        return "Paid & Closed", debug_steps

    # Step 7: Adjusted & Closed
    if payment_status == "Adjusted":
        debug_steps.append("Step 7: Adjusted claim")
        return "Adjusted & Closed", debug_steps

    # Step 8: Patient Signature Requested npp signature required
    if ar_status == "Open - Pt AR" and \
            ('signature required' in schedule_track or 'npp' in schedule_track):
        debug_steps.append("Step 8: Patient signature required")
        return "Pt Sign requested", debug_steps

    # Step 9: Billed to Patient - Primary
    if (payor == 'patient' and pri_payor == 'patient' and \
        not any(x in schedule_track for x in ['waystar', 'denials', 'automatic crossover'])) or \
            (ar_status == "Open - Pt AR" and pri_payor == 'patient'):
        debug_steps.append("Step 9: Billed to patient (primary)")
        return "Billed to Pt - Pri", debug_steps

    # Step 10: Billed to Patient - Secondary
    if ar_status == "Open - Pt AR" and \
            payor == 'patient' and pri_payor != 'patient':
        debug_steps.append("Step 10: Billed to patient (secondary)")
        return "Billed to Pt - Sec", debug_steps

    # Step 11: Billed to Insurance - Primary
    if ar_status == "Open - Ins AR" and \
            payor == pri_payor and \
            'automatic crossover' not in schedule_track:
        debug_steps.append("Step 11: Billed to insurance (primary)")
        return "Billed to Ins - Pri", debug_steps

    # Step 12: Billed to Insurance - Secondary
    if ar_status == "Open - Ins AR":
        debug_steps.append("Step 12: Billed to insurance (secondary)")
        return "Billed to Ins - Sec", debug_steps

    debug_steps.append("No matching claim status found - defaulting")
    return "Unclassified", debug_steps


def classify_payment_status(row):
    balance = float(getattr(row, 'balance_due', 0) or 0)
    charge = float(getattr(row, 'net_charges', 0) or 0)
    payments = float(getattr(row, 'payments', 0) or 0)
    status = (getattr(row, 'status', '') or '').lower()

    if balance < 0:
        return "Negative balance"
    elif balance == 0 and charge == 0 and status in ['canceled', 'closed']:
        return "Canceled Trip"
    elif balance == 0 and charge > 0 and payments > 0:
        return "Paid & Closed"
    elif balance == 0 and payments == 0:
        return "Adjusted"
    elif payments > 0:
        return "Partially paid"
    elif charge != 0 or balance != 0:
        return "Unpaid"
    return ""


def convert_to_serializable(value):
    """Convert pandas and numpy types to Python native types"""
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, (np.integer)):
        return int(value)
    if isinstance(value, (np.floating)):
        return float(value)
    if isinstance(value, (np.ndarray)):
        return value.tolist()
    return value


def sanitize_column_name(col_name):
    """Sanitize column name to avoid issues with SQL syntax."""
    return re.sub(r'\W|^(?=\d)', '_', col_name)


def convert_to_sql_compatible(value):
    """Convert values to SQL-compatible formats."""
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return value
    return str(value)


def classify_ar_status(row, payment_status):
    status = (getattr(row, 'status', '') or '').lower()
    payor = (getattr(row, 'cur_pay_category', '') or '').lower()
    pri_payor = (getattr(row, 'pri_payor_category', '') or '').lower()
    schedule_track = (getattr(row, 'schedule_track', '') or '').lower()

    balance = float(getattr(row, 'balance_due', 0) or 0)
    charge = float(getattr(row, 'net_charges', 0) or 0)

    if payment_status == "Negative balance":
        return "Negative Ins AR"
    elif (
            (balance == 0 and charge == 0 and status in ['canceled', 'closed']) or
            payment_status == "Canceled Trip"
    ):
        return "Canceled Trip"
    elif payment_status == "Paid & Closed" and pri_payor == 'patient' and payor == 'patient':
        return "Closed - Pt Pri"
    elif payment_status == "Paid & Closed":
        return "Closed - Ins Pri"
    elif payment_status == "Adjusted":
        return "Adjusted & Closed"
    elif payor == "patient" and "denials" not in schedule_track and "waystar" not in schedule_track:
        return "Open - Pt AR"
    return "Open - Ins AR"

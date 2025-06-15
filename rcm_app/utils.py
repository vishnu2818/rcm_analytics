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

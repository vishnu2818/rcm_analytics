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
    debug = []

    schedule_track = (row.schedule_track or '').lower()
    status = (row.status or '').lower()
    team = (row.team or '').lower()
    event = (row.event_step or '').lower()
    coll = (row.coll or '').strip().upper()

    debug.append(f"Schedule/Track: {schedule_track}")
    debug.append(f"Status: {status}")
    debug.append(f"Team: {team}")
    debug.append(f"Event/Step: {event}")
    debug.append(f"Coll: {coll}")

    # 💡 Add your logic here:
    if ar_status == "Canceled Trip":
        return "Canceled", debug

    if "denial" in schedule_track:
        return "Denial WQ", debug

    if "waystar" in schedule_track:
        return "Waystar WQ", debug

    if coll == "YES":
        return "Collections", debug

    if team == "coding":
        return "Coding Review", debug

    if "appeal" in schedule_track:
        return "Appeal WQ", debug

    if event in ["submitted", "resubmitted"]:
        return "Submitted", debug

    return "Pending Review", debug

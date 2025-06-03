# from django import template
#
# register = template.Library()
#
# @register.filter
# def get_item(value, key):
#     """Custom filter to retrieve item from dictionary by key."""
#     return value.get(key)

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(key)


from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(key)


@register.filter
def payment_status(row):
    data = row.data
    balance = data.get("Balance amt", 0)
    charge = data.get("Charge amt", 0)
    status = data.get("Status", "").lower()
    payments = data.get("Payments", 0)
    payment_amt = data.get("Payment Amt", 0)

    try:
        balance = float(balance)
        charge = float(charge)
        payments = float(payments)
        payment_amt = float(payment_amt)
    except (TypeError, ValueError):
        return "Unknown"

    if balance < 0:
        return "Negative balance"
    elif balance == 0 and charge == 0 and status in ["canceled", "closed"]:
        return "Canceled Trip"
    elif balance == 0 and charge > 0 and payments > 0:
        return "Paid & Closed"
    elif balance == 0 and payment_amt == 0:
        return "Adjusted"
    elif payments > 0:
        return "Partially paid"
    else:
        return "Unpaid"


@register.filter
def ar_status(row):
    data = row.data
    payment_status_val = payment_status(row)
    balance = data.get("Balance amt", 0)
    charge = data.get("Charge amt", 0)
    status = data.get("Status", "").lower()
    primary_payor = data.get("Primary Payor Category", "").lower()
    current_payor = data.get("Current Payor category", "").lower()
    schedule_track = str(data.get("schedule/Track", "")).lower()

    try:
        balance = float(balance)
        charge = float(charge)
    except (TypeError, ValueError):
        return "Unknown"

    if payment_status_val == "Negative balance":
        return "Negative Ins AR"
    elif (balance == 0 and charge == 0 and status in ["canceled", "closed"]) or payment_status_val == "Canceled Trip":
        return "Canceled Trip"
    elif payment_status_val == "Paid & Closed" and primary_payor == "patient" and current_payor == "patient":
        return "Closed - Pt Pri"
    elif payment_status_val == "Paid & Closed":
        return "Closed - Ins Pri"
    elif payment_status_val == "Adjusted":
        return "Adjusted & Closed"
    elif current_payor == "patient" and not any(track in schedule_track for track in ["denials", "waystar"]):
        return "Open - Pt AR"
    else:
        return "Open - Ins AR"

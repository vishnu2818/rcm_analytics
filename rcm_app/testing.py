import os
import django

# SET THIS TO YOUR PROJECT'S SETTINGS MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rcm_analytics.settings')
django.setup()

# Now you can safely import Django models
from rcm_app.models import ExcelData
import pandas as pd

def parse_date(value):
    try:
        return pd.to_datetime(value, errors='coerce').date()
    except Exception:
        return None

def deserialize_all_fields():
    updated = 0

    for row in ExcelData.objects.all():
        data = row.data

        # Example mappings (must match sanitized model field names)
        row.company = data.get('Company')
        row.dos = parse_date(data.get('DOS'))
        row.dosym = data.get('DOSYM')
        row.run = data.get('Run #')
        row.inc = data.get('Inc #t')
        row.cust = data.get('Cust.')
        row.dob = parse_date(data.get('DOB'))
        row.status = data.get('Status')
        row.prim_pay = data.get('Prim Pay')
        row.pri_payor_category = data.get('Pri Payor Category')
        row.cur_pay = data.get('Cur Pay')
        row.cur_pay_category = data.get('Cur Pay Category')
        row.schedule_track = data.get('Schedule/Track')
        row.event_step = data.get('Event/Step')
        row.coll = data.get('Coll')
        row.gross_charges = data.get('Gross Charges')
        row.contr_allow = data.get('Contr Allow')
        row.net_charges = data.get('Net Charges')
        row.revenue_adjustments = data.get('Revenue Adjustments')
        row.payments = data.get('Payments')
        row.write_offs = data.get('Write-Offs')
        row.refunds = data.get('Refunds')
        row.balance_due = data.get('Balance Due')
        row.aging_date = parse_date(data.get('Aging Date'))
        row.last_event_date = parse_date(data.get('Last Event Date'))
        row.ordering_facility = data.get('Ordering Facility')
        row.vehicle = data.get('Vehicle')
        row.call_type = data.get('Call Type')
        row.priority = data.get('Priority')
        row.call_type_priority = data.get('Call Type - Priority')
        row.primary_icd = data.get('Primary ICD')
        row.loaded_miles = data.get('Loaded Miles')
        row.pickup_facility = data.get('Pickup Facility')
        row.pickup_modifier = data.get('Pickup Modifier')
        row.pickup_address = data.get('Pickup Address')
        row.pickup_city = data.get('Pickup City')
        row.pickup_state = data.get('Pickup State')
        row.pickup_zip = data.get('Pickup Zip')
        row.dropoff_facility = data.get('DropOff Facility')
        row.dropoff_modifier = data.get('DropOff Modifier')
        row.dropoff_address = data.get('DropOff Address')
        row.dropoff_city = data.get('DropOff City')
        row.dropoff_state = data.get('DropOff State')
        row.dropoff_zip = data.get('DropOff Zip')
        row.import_date = parse_date(data.get('Import Date'))
        row.import_date_ym = data.get('Import Date YM')
        row.med_nec = data.get('Med Nec')
        row.accident_type = data.get('Accident Type')
        row.assigned_group = data.get('Assigned Group')
        row.location = data.get('Location')
        row.last_modified_date = parse_date(data.get('Last Modified Date'))
        row.last_modified_by = data.get('Last Modified By')
        row.team = data.get('Team')
        row.job = data.get('Job')
        row.emsmartid = data.get('EMSmartID')
        row.prior_auth = data.get('Prior Auth')
        row.payment_status = data.get('Payment Status')
        row.ar_status = data.get('AR Status')
        row.claim_status = data.get('Claim Status')

        row.save()
        updated += 1

    print(f"{updated} records updated.")

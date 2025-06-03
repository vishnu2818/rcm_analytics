from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    uploads = ExcelUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'home.html', {'uploads': uploads})


from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import *


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create profile manually (instead of relying on signal)
            Profile.objects.create(
                user=user,

                company_name=form.cleaned_data['company_name'],
                company_email=form.cleaned_data['company_email'],
                phone=form.cleaned_data['phone'],
                avg_claim_rate_per_month=form.cleaned_data['avg_claim_rate_per_month'],
                heard_about_us=form.cleaned_data['heard_about_us']
            )

            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


import re


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


import numpy as np


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


# @login_required
# def upload_excel(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 file = request.FILES['file']
#
#                 # Read Excel file
#                 df = pd.read_excel(file, engine='openpyxl')
#
#                 # Convert all values to JSON-serializable format
#                 serializable_data = []
#                 for _, row in df.iterrows():
#                     serializable_row = {col: convert_to_serializable(row[col]) for col in df.columns}
#                     serializable_data.append(serializable_row)
#
#                 # Create ExcelUpload object with current user
#                 upload = ExcelUpload.objects.create(
#                     user=request.user,  # Assign user
#                     file_name=file.name,
#                     row_count=len(df),
#                     columns={col: str(df[col].dtype) for col in df.columns}
#                 )
#
#                 # Bulk insert ExcelData
#                 ExcelData.objects.bulk_create([
#                     ExcelData(upload=upload, data=row_data)
#                     for row_data in serializable_data
#                 ])
#
#                 return render(request, 'upload_success.html', {
#                     'upload': upload,
#                     'columns': df.columns.tolist(),
#                     'row_count': len(df)
#                 })
#
#             except Exception as e:
#                 error_msg = str(e)
#                 if 'No such file or directory' in error_msg:
#                     error_msg = "Please select a file to upload."
#                 return render(request, 'upload.html', {
#                     'form': form,
#                     'error': f'Error processing file: {error_msg}'
#                 })
#     else:
#         form = ExcelUploadForm()
#
#     return render(request, 'upload.html', {'form': form})

# recently modified code

from decimal import Decimal, InvalidOperation
from datetime import datetime
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ExcelUploadForm
from .models import ExcelUpload, ExcelData


@login_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')

                # Convert all values to JSON-serializable format
                serializable_data = []
                for _, row in df.iterrows():
                    serializable_row = {col: convert_to_serializable(row[col]) for col in df.columns}
                    serializable_data.append(serializable_row)

                upload = ExcelUpload.objects.create(
                    user=request.user,
                    file_name=file.name,
                    row_count=len(df),
                    columns={col: str(df[col].dtype) for col in df.columns}
                )

                created_objects = []
                for row_data in serializable_data:
                    obj = ExcelData(
                        upload=upload,

                        company=row_data.get("Company", "Unknown"),
                        dos=parse_date(row_data.get("DOS")),
                        dosym=row_data.get("DOSYM", "Unknown"),
                        run_number=row_data.get("Run #", "Unknown"),
                        inc_number=row_data.get("Inc #t", "Unknown"),
                        customer=row_data.get("Cust.", None),
                        dob=row_data.get("DOB", None),
                        status=row_data.get("Status", "Unknown"),

                        prim_pay=row_data.get("Prim Pay", "Unknown"),
                        pri_payor_category=row_data.get("Pri Payor Category", "Unknown"),
                        cur_pay=row_data.get("Cur Pay", "Unknown"),
                        cur_pay_category=row_data.get("Cur Pay Category", "Unknown"),

                        schedule_track=row_data.get("Schedule/Track", "Unknown"),
                        event_step=row_data.get("Event/Step", "Unknown"),
                        coll=row_data.get("Coll", "NO"),

                        gross_charges=parse_decimal(row_data.get("Gross Charges")),
                        contr_allow=parse_decimal(row_data.get("Contr Allow")),
                        net_charges=parse_decimal(row_data.get("Net Charges")),
                        revenue_adjustments=parse_decimal(row_data.get("Revenue Adjustments")),
                        payments=parse_decimal(row_data.get("Payments")),
                        write_offs=parse_decimal(row_data.get("Write-Offs")),
                        refunds=parse_decimal(row_data.get("Refunds")),
                        balance_due=parse_decimal(row_data.get("Balance Due")),

                        aging_date=parse_date(row_data.get("Aging Date")),
                        last_event_date=parse_date(row_data.get("Last Event Date")),

                        ordering_facility=row_data.get("Ordering Facility", None),
                        vehicle=str(row_data.get("Vehicle", "Unknown")),

                        call_type=row_data.get("Call Type", "Unknown"),
                        priority=row_data.get("Priority", "Unknown"),
                        call_type_priority=row_data.get("Call Type - Priority", "Unknown"),

                        primary_icd=row_data.get("Primary ICD", "Unknown"),
                        loaded_miles=parse_decimal(row_data.get("Loaded Miles", 0.0)),

                        pickup_facility=row_data.get("Pickup Facility", None),
                        pickup_modifier=row_data.get("Pickup Modifier", "Unknown"),
                        pickup_address=row_data.get("Pickup Address", None),
                        pickup_city=row_data.get("Pickup City", "Unknown"),
                        pickup_state=row_data.get("Pickup State", "NA"),
                        pickup_zip=str(row_data.get("Pickup Zip", "00000")),

                        dropoff_facility=row_data.get("DropOff Facility", "Unknown"),
                        dropoff_modifier=row_data.get("DropOff Modifier", "Unknown"),
                        dropoff_address=row_data.get("DropOff Address", None),
                        dropoff_city=row_data.get("DropOff City", "Unknown"),
                        dropoff_state=row_data.get("DropOff State", "NA"),
                        dropoff_zip=str(row_data.get("DropOff Zip", "00000")),

                        import_date=parse_date(row_data.get("Import Date")),
                        import_date_ym=row_data.get("Import Date YM", "Unknown"),

                        med_nec=row_data.get("Med Nec", "Unknown"),
                        accident_type=row_data.get("Accident Type", None),

                        assigned_group=str(row_data.get("Assigned Group", None)),
                        location=row_data.get("Location", "Unknown"),

                        last_modified_date=parse_date(row_data.get("Last Modified Date")),
                        last_modified_by=row_data.get("Last Modified By", "Unknown"),

                        team=row_data.get("Team", "Unknown"),
                        job=row_data.get("Job", "Unknown"),
                        emsmart_id=row_data.get("EMSmartID", "Unknown"),
                        prior_auth=row_data.get("Prior Auth", None),
                    )
                    created_objects.append(obj)

                ExcelData.objects.bulk_create(created_objects)

                return render(request, 'upload_success.html', {
                    'upload': upload,
                    'columns': df.columns.tolist(),
                    'row_count': len(created_objects)
                })

            except Exception as e:
                return render(request, 'upload.html', {
                    'form': form,
                    'error': f'Error: {str(e)}'
                })

    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})


# Helper functions
def parse_date(val):
    try:
        if pd.isna(val):
            return datetime(2000, 1, 1).date()
        if isinstance(val, datetime):
            return val.date()
        return pd.to_datetime(val).date()
    except Exception:
        return datetime(2000, 1, 1).date()


def parse_decimal(val):
    try:
        if pd.isna(val) or val == '':
            return Decimal('0.00')
        return Decimal(str(val))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal('0.00')


# def convert_to_serializable(val):
#     if isinstance(val, (datetime, pd.Timestamp)):
#         return val.isoformat()
#     if pd.isna(val):
#         return None
#     return val


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


from .models import ExcelData

from django.shortcuts import render
from django.http import HttpResponse
from .models import ExcelData
from django.forms.models import model_to_dict


def test_display_data_verbose(request):
    upload_id = request.GET.get('upload_id')

    if not upload_id:
        return HttpResponse("No upload selected. Please choose an upload file.", status=400)

    # Fetch first 50 rows for selected upload
    queryset = ExcelData.objects.filter(upload__id=upload_id, upload__user=request.user)[:50]

    if not queryset.exists():
        return HttpResponse("No data found for the selected upload or you do not have permission.", status=404)

    processed_data = []

    print("\n======= STARTING CLASSIFICATION PROCESS =======")

    for i, row in enumerate(queryset, 1):
        balance = row.balance_due or 0
        charge = row.net_charges or 0
        payments = row.payments or 0
        status = (row.status or '').lower()
        payor = (row.cur_pay_category or '').lower()
        pri_payor = (row.pri_payor_category or '').lower()
        schedule_track = (row.schedule_track or '').lower()

        print(f"\n--- Row {i} ---")
        print(f"Key Values: Balance={balance}, Charge={charge}, Payments={payments}, Status='{status}'")
        print(f"Payor Info: Current='{payor}', Primary='{pri_payor}', Schedule='{schedule_track}'")

        # 1. Payment Status Classification
        print("\n1. Determining Payment Status:")
        if balance < 0:
            ps = "Negative balance"
            print(f"  - Rule: Balance ({balance}) < 0 → '{ps}'")
        elif balance == 0 and charge == 0 and status in ['canceled', 'closed']:
            ps = "Canceled Trip"
            print(f"  - Rule: Zero balance & charge + status '{status}' → '{ps}'")
        elif balance == 0 and charge > 0 and payments > 0:
            ps = "Paid & Closed"
            print(f"  - Rule: Zero balance with payments → '{ps}'")
        elif balance == 0 and payments == 0:
            ps = "Adjusted"
            print(f"  - Rule: Zero balance without payments → '{ps}'")
        elif payments > 0:
            ps = "Partially paid"
            print(f"  - Rule: Payments exist but balance remains → '{ps}'")
        else:
            ps = "Unpaid"
            print(f"  - Rule: Default case → '{ps}'")

        # 2. AR Status Classification
        print("\n2. Determining AR Status:")
        if ps == "Negative balance":
            ars = "Negative Ins AR"
            print(f"  - Rule: Payment Status is '{ps}' → '{ars}'")
        elif (balance == 0 and charge == 0 and status in ['canceled', 'closed']) or ps == "Canceled Trip":
            ars = "Canceled Trip"
            print(f"  - Rule: Canceled trip conditions → '{ars}'")
        elif ps == "Paid & Closed" and pri_payor == 'patient' and payor == 'patient':
            ars = "Closed - Pt Pri"
            print(f"  - Rule: Paid & patient primary → '{ars}'")
        elif ps == "Paid & Closed":
            ars = "Closed - Ins Pri"
            print(f"  - Rule: Paid & non-patient primary → '{ars}'")
        elif ps == "Adjusted":
            ars = "Adjusted & Closed"
            print(f"  - Rule: Payment Status is '{ps}' → '{ars}'")
        elif payor == "patient" and "denials" not in schedule_track and "waystar" not in schedule_track:
            ars = "Open - Pt AR"
            print(f"  - Rule: Patient payor without denials → '{ars}'")
        else:
            ars = "Open - Ins AR"
            print(f"  - Rule: Default case → '{ars}'")

        # 3. Claim Status Classification
        print("\n3. Determining Claim Status:")
        cs, cs_debug = classify_claim_status(row, ps, ars)
        for step in cs_debug:
            print(f"  - {step}")
        print(f"  - Final Claim Status: '{cs}'")

        print(f"\nFinal Classification: Payment='{ps}', AR='{ars}', Claim='{cs}'")

        # processed_data.append({
        #     'row': row,  # you can use `row.<field>` in template if needed
        #     'Payment Status': ps,
        #     'AR Status': ars,
        #     'Claim Status': cs
        # })

        row_data = model_to_dict(row)
        row_data.update({
            'Payment Status': ps,
            'AR Status': ars,
            'Claim Status': cs,
        })
        processed_data.append(row_data)

    print("\n======= CLASSIFICATION COMPLETE =======")

    return render(request, 'testing.html', {'data': processed_data})


import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse

def download_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ExcelData Preview"

    rows = ExcelData.objects.filter(upload__user=request.user)[:50]

    data = []
    for row in rows:
        ps = classify_payment_status(row)
        ars = classify_ar_status(row, ps)

        row_dict = {
            'Company': row.company,
            'Date of Service': row.dos,
            'DOS YM': row.dosym,
            'Run Number': row.run_number,
            'Incident Number': row.inc_number,
            'Customer': row.customer,
            'DOB': row.dob,
            'Status': row.status,
            'Primary Payor': row.prim_pay,
            'Primary Payor Category': row.pri_payor_category,
            'Current Payor': row.cur_pay,
            'Current Payor Category': row.cur_pay_category,
            'Schedule/Track': row.schedule_track,
            'Event Step': row.event_step,
            'COLL': row.coll,
            'Gross Charges': float(row.gross_charges),
            'Contractual Allowance': float(row.contr_allow),
            'Net Charges': float(row.net_charges),
            'Revenue Adjustments': float(row.revenue_adjustments),
            'Payments': float(row.payments),
            'Write-offs': float(row.write_offs),
            'Refunds': float(row.refunds),
            'Balance Due': float(row.balance_due),
            'Aging Date': row.aging_date,
            'Last Event Date': row.last_event_date,
            'Ordering Facility': row.ordering_facility,
            'Vehicle': row.vehicle,
            'Call Type': row.call_type,
            'Priority': row.priority,
            'Call Type Priority': row.call_type_priority,
            'Primary ICD': row.primary_icd,
            'Loaded Miles': float(row.loaded_miles),
            'Pickup Facility': row.pickup_facility,
            'Pickup Modifier': row.pickup_modifier,
            'Pickup Address': row.pickup_address,
            'Pickup City': row.pickup_city,
            'Pickup State': row.pickup_state,
            'Pickup ZIP': row.pickup_zip,
            'Dropoff Facility': row.dropoff_facility,
            'Dropoff Modifier': row.dropoff_modifier,
            'Dropoff Address': row.dropoff_address,
            'Dropoff City': row.dropoff_city,
            'Dropoff State': row.dropoff_state,
            'Dropoff ZIP': row.dropoff_zip,
            'Import Date': row.import_date,
            'Import Date YM': row.import_date_ym,
            'Medical Necessity': row.med_nec,
            'Accident Type': row.accident_type,
            'Assigned Group': row.assigned_group,
            'Location': row.location,
            'Last Modified Date': row.last_modified_date,
            'Last Modified By': row.last_modified_by,
            'Team': row.team,
            'Job': row.job,
            'EMSmart ID': row.emsmart_id,
            'Prior Auth': row.prior_auth,
            'Payment Status': ps,
            'AR Status': ars,
        }

        data.append(row_dict)

    if not data:
        return HttpResponse("No data to export.", status=400)

    # Write headers
    headers = list(data[0].keys())
    ws.append(headers)

    # Write rows
    for row in data:
        ws.append([row.get(col, '') for col in headers])

    # Adjust column widths
    for col_num, col in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(col_num)].width = 20

    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=excel_data_preview.xlsx'
    wb.save(response)
    return response




from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def download_pdf(request):
    rows = ExcelData.objects.filter(upload__user=request.user)[:50]

    data = []
    for row in rows:
        ps = classify_payment_status(row)
        ars = classify_ar_status(row, ps)

        row_dict = {
            'Company': row.company,
            'Date of Service': row.dos,
            'DOS YM': row.dosym,
            'Run Number': row.run_number,
            'Incident Number': row.inc_number,
            'Customer': row.customer,
            'DOB': row.dob,
            'Status': row.status,
            'Primary Payor': row.prim_pay,
            'Primary Payor Category': row.pri_payor_category,
            'Current Payor': row.cur_pay,
            'Current Payor Category': row.cur_pay_category,
            'Schedule/Track': row.schedule_track,
            'Event Step': row.event_step,
            'COLL': row.coll,
            'Gross Charges': float(row.gross_charges),
            'Contractual Allowance': float(row.contr_allow),
            'Net Charges': float(row.net_charges),
            'Revenue Adjustments': float(row.revenue_adjustments),
            'Payments': float(row.payments),
            'Write-offs': float(row.write_offs),
            'Refunds': float(row.refunds),
            'Balance Due': float(row.balance_due),
            'Aging Date': row.aging_date,
            'Last Event Date': row.last_event_date,
            'Ordering Facility': row.ordering_facility,
            'Vehicle': row.vehicle,
            'Call Type': row.call_type,
            'Priority': row.priority,
            'Call Type Priority': row.call_type_priority,
            'Primary ICD': row.primary_icd,
            'Loaded Miles': float(row.loaded_miles),
            'Pickup Facility': row.pickup_facility,
            'Pickup Modifier': row.pickup_modifier,
            'Pickup Address': row.pickup_address,
            'Pickup City': row.pickup_city,
            'Pickup State': row.pickup_state,
            'Pickup ZIP': row.pickup_zip,
            'Dropoff Facility': row.dropoff_facility,
            'Dropoff Modifier': row.dropoff_modifier,
            'Dropoff Address': row.dropoff_address,
            'Dropoff City': row.dropoff_city,
            'Dropoff State': row.dropoff_state,
            'Dropoff ZIP': row.dropoff_zip,
            'Import Date': row.import_date,
            'Import Date YM': row.import_date_ym,
            'Medical Necessity': row.med_nec,
            'Accident Type': row.accident_type,
            'Assigned Group': row.assigned_group,
            'Location': row.location,
            'Last Modified Date': row.last_modified_date,
            'Last Modified By': row.last_modified_by,
            'Team': row.team,
            'Job': row.job,
            'EMSmart ID': row.emsmart_id,
            'Prior Auth': row.prior_auth,
            'Payment Status': ps,
            'AR Status': ars,
        }

        data.append(row_dict)

    if not data:
        return HttpResponse("No data available for PDF generation", status=400)

    template = get_template('pdf_template.html')
    html = template.render({'data': data})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="excel_data_preview.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response



# from collections import Counter, defaultdict
# from datetime import datetime
#
#
# def dashboard_view(request):
#     rows = ExcelData.objects.filter(upload__user=request.user)
#
#     processed = []
#     net_charges = 0
#     total_payments = 0
#     total_balance = 0
#     ar_days = []
#
#     for row in rows:
#         d = row.data
#         ps = classify_payment_status(d)
#         ars = classify_ar_status(d, ps)
#
#         net = float(d.get('Net Charges', 0))
#         paid = float(d.get('Payments', 0))
#         balance = float(d.get('Balance Due', 0))
#
#         net_charges += net
#         total_payments += paid
#         total_balance += balance
#
#         # Aging Days
#         aging_str = d.get('Aging Date')
#         if aging_str:
#             try:
#                 aging_date = datetime.strptime(aging_str, "%Y-%m-%d")
#                 ar_days.append((datetime.now() - aging_date).days)
#             except Exception:
#                 pass
#
#         d['Payment Status'] = ps
#         d['AR Status'] = ars
#         processed.append(d)
#
#     payment_counts = Counter(d['Payment Status'] for d in processed)
#     ar_counts = Counter(d['AR Status'] for d in processed)
#     payor_counts = Counter(d.get('Pri Payor Category', 'Unknown') for d in processed)
#     track_counts = Counter(d.get('Schedule/Track', 'Unknown') for d in processed)
#
#     import_trends = defaultdict(lambda: {'charges': 0, 'payments': 0})
#     for d in processed:
#         ym = d.get('Import Date YM')
#         import_trends[ym]['charges'] += float(d.get('Net Charges', 0))
#         import_trends[ym]['payments'] += float(d.get('Payments', 0))
#
#     avg_ar_days = round(sum(ar_days) / len(ar_days), 1) if ar_days else 0
#
#     return render(request, 'dashboard.html', {
#         'total_claims': len(processed),
#         'net_charges': net_charges,
#         'total_payments': total_payments,
#         'total_balance': total_balance,
#         'avg_ar_days': avg_ar_days,
#         'payment_counts': dict(payment_counts),
#         'ar_counts': dict(ar_counts),
#         'payor_counts': dict(payor_counts),
#         'track_counts': dict(track_counts),
#         'import_trends': dict(import_trends),
#     })

# new code

from collections import Counter, defaultdict
from datetime import datetime
from django.shortcuts import render


def dashboard_view(request):
    rows = ExcelData.objects.filter(upload__user=request.user)

    processed = []
    net_charges = 0
    total_payments = 0
    total_balance = 0
    ar_days = []

    for row in rows:
        # Accessing direct model fields
        ps = classify_payment_status(row)
        ars = classify_ar_status(row, ps)

        net = float(getattr(row, 'net_charges', 0))
        paid = float(getattr(row, 'payments', 0))
        balance = float(getattr(row, 'balance_due', 0))

        net_charges += net
        total_payments += paid
        total_balance += balance

        # Aging Days
        aging_str = getattr(row, 'aging_date', None)
        if aging_str:
            try:
                aging_date = datetime.strptime(str(aging_str), "%Y-%m-%d")
                ar_days.append((datetime.now() - aging_date).days)
            except Exception:
                pass

        # Build dict of all fields for display
        d = {
            'Patient Name': getattr(row, 'patient_name', ''),
            'Net Charges': net,
            'Payments': paid,
            'Balance Due': balance,
            'Status': getattr(row, 'status', ''),
            'Current Payor Category': getattr(row, 'cur_pay_category', ''),
            'Primary Payor Category': getattr(row, 'pri_payor_category', ''),
            'Schedule/Track': getattr(row, 'schedule_track', ''),
            'Import Date YM': getattr(row, 'import_date_ym', ''),
            'Aging Date': aging_str,
            'Payment Status': ps,
            'AR Status': ars,
        }

        processed.append(d)

    # Aggregations
    payment_counts = Counter(d['Payment Status'] for d in processed)
    ar_counts = Counter(d['AR Status'] for d in processed)
    payor_counts = Counter(d.get('Primary Payor Category', 'Unknown') for d in processed)
    track_counts = Counter(d.get('Schedule/Track', 'Unknown') for d in processed)

    import_trends = defaultdict(lambda: {'charges': 0, 'payments': 0})
    for d in processed:
        ym = d.get('Import Date YM')
        import_trends[ym]['charges'] += float(d.get('Net Charges', 0))
        import_trends[ym]['payments'] += float(d.get('Payments', 0))

    avg_ar_days = round(sum(ar_days) / len(ar_days), 1) if ar_days else 0

    return render(request, 'dashboard.html', {
        'total_claims': len(processed),
        'net_charges': net_charges,
        'total_payments': total_payments,
        'total_balance': total_balance,
        'avg_ar_days': avg_ar_days,
        'payment_counts': dict(payment_counts),
        'ar_counts': dict(ar_counts),
        'payor_counts': dict(payor_counts),
        'track_counts': dict(track_counts),
        'import_trends': dict(import_trends),
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from django.http import JsonResponse


@login_required
def start_chat(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    rooms = ChatRoom.objects.filter(users=request.user).filter(users=target_user)
    if rooms.exists():
        room = rooms.first()
    else:
        room = ChatRoom.objects.create()
        room.users.add(request.user, target_user)
    return redirect('chat_room', room_id=room.id)


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.users.all():
        return redirect('user_list')
    messages = Message.objects.filter(room=room).order_by('timestamp')
    return render(request, 'chat_room.html', {'room': room, 'messages': messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        room_id = request.POST.get('room_id')
        room = ChatRoom.objects.get(id=room_id)
        message = Message.objects.create(room=room, sender=request.user, content=content)
        return JsonResponse({'status': 'Message Sent'})
    return JsonResponse({'status': 'Failed'})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

from rcm_app.models import QAAudit
audits = QAAudit.objects.all()
print(audits.count())  # should be > 0

from django import forms
from .models import IncidentTicket

class TicketSubmissionForm(forms.ModelForm):
    class Meta:
        model = IncidentTicket
        fields = ['title', 'description', 'severity', 'affected_asset']
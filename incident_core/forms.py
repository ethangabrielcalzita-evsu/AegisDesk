from django import forms
from .models import IncidentTicket

class TicketSubmissionForm(forms.ModelForm):
    class Meta:
        model = IncidentTicket
        fields = ['title', 'description', 'category', 'severity', 'affected_asset']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class NistTriageForm(forms.ModelForm):
    class Meta:
        model = IncidentTicket
        fields = ['nist_stage']
        labels = {
            'nist_stage': 'NIST Incident Response Stage',
        }

class BulkCloseForm(forms.Form):
    selected_tickets = forms.ModelMultipleChoiceField(
        queryset=IncidentTicket.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Select tickets to close',
    )

    def __init__(self, *args, queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['selected_tickets'].queryset = queryset
from rest_framework import serializers
from .models import IncidentTicket, Asset

class AutomatedIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentTicket
        fields = ['title', 'description', 'severity', 'affected_asset', 'nist_stage']

    def create(self, validated_data):
        ticket = IncidentTicket(**validated_data)
        ticket._current_user = "Remote_Monitoring_API_Agent"
        ticket.save()
        return ticket
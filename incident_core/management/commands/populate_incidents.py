# incident_core/management/commands/populate_incidents.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from incident_core.models import Asset, IncidentTicket

class Command(BaseCommand):
    help = 'Populates baseline enterprise assets and NIST tickets.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing AegisDesk environment population...")
        
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@aegisdesk.local", "SecurePassword123!")
            self.stdout.write("Created Superuser: admin / SecurePassword123!")

        server_asset, _ = Asset.objects.get_or_create(
            name="Primary_AD_Server", 
            asset_type="SERVER", 
            ip_address="10.0.1.4"
        )
        
        cloud_asset, _ = Asset.objects.get_or_create(
            name="AWS_S3_PII_Bucket", 
            asset_type="CLOUD", 
            ip_address="192.168.50.22"
        )
        
        ticket1 = IncidentTicket.objects.create(
            title="Brute Force Attempts Detected",
            description="Multiple bad auth password queries inside 60 seconds.",
            nist_stage="DETECTION_ANALYSIS",
            severity="HIGH",
            affected_asset=server_asset
        )
        ticket1._current_user = "System_Initializer"
        ticket1.save()

        ticket2 = IncidentTicket.objects.create(
            title="S3 Object Exposure Leak",
            description="External inspection flagged write parameters visible publicly.",
            nist_stage="CONTAINMENT_ERADICATION",
            severity="CRITICAL",
            affected_asset=cloud_asset
        )
        ticket2._current_user = "System_Initializer"
        ticket2.save()

        self.stdout.write(self.style.SUCCESS("AegisDesk baseline records successfully configured!"))
import logging
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger('incident_audit')

class Asset(models.Model):
    ASSET_TYPES = [
        ('SERVER', 'Enterprise Server'),
        ('WORKSTATION', 'Employee Workstation'),
        ('NETWORK', 'Network Router/Switch'),
        ('CLOUD', 'Cloud Repository'),
    ]
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class IncidentTicket(models.Model):
    NIST_STAGES = [
        ('PREPARATION', '1. Preparation'),
        ('DETECTION_ANALYSIS', '2. Detection & Analysis'),
        ('CONTAINMENT_ERADICATION', '3. Containment, Eradication & Recovery'),
        ('POST_INCIDENT', '4. Post-Incident Activity'),
        ('CLOSED', '5. Resolved / Closed'),
    ]

    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    CATEGORY_CHOICES = [
        ('IT_SUPPORT', 'IT Support'),
        ('SECURITY_BREACH', 'Security Breach'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='IT_SUPPORT')
    nist_stage = models.CharField(max_length=30, choices=NIST_STAGES, default='PREPARATION')
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='LOW')
    affected_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='incidents')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.severity}] {self.title} - Status: {self.get_nist_stage_display()}"

    def save(self, *args, **kwargs):
        current_user = getattr(self, '_current_user', 'System_Automated_API')
        
        if self.pk:
            old_instance = IncidentTicket.objects.get(pk=self.pk)
            if old_instance.nist_stage != self.nist_stage:
                logger.info(
                    f"Ticket #{self.id} modified. Stage altered from '{old_instance.nist_stage}' to '{self.nist_stage}'.",
                    extra={'user': current_user}
                )
        else:
            logger.info(
                f"New incident registered. Title: '{self.title}' for Asset: {self.affected_asset.name}",
                extra={'user': current_user}
            )
        super().save(*args, **kwargs)
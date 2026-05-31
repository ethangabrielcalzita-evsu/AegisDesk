from django.contrib import admin
from .models import Asset, IncidentTicket

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'ip_address')
    list_filter = ('asset_type',)
    search_fields = ('name', 'ip_address')

@admin.register(IncidentTicket)
class IncidentTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'affected_asset', 'severity', 'nist_stage', 'updated_at')
    list_filter = ('nist_stage', 'severity', 'created_at')
    search_fields = ('title', 'description', 'affected_asset__name')
    actions = ['bulk_close_resolved_tickets']

    @admin.action(description='Bulk-close selected resolved operational tickets')
    def bulk_close_resolved_tickets(self, request, queryset):
        for ticket in queryset:
            ticket._current_user = f"Admin_Mgr_{request.user.username}"
            ticket.nist_stage = 'CLOSED'
            ticket.save()
        
        self.message_user(request, f"Successfully marked {queryset.count()} tickets as Resolved / Closed.")
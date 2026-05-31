from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .api_views import AutomatedIncidentIngestView

urlpatterns = [
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('submit/success/', views.ticket_success, name='ticket_success'),
    
    # JWT Auth & API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/log-incident/', AutomatedIncidentIngestView.as_view(), name='api_log_incident'),
]
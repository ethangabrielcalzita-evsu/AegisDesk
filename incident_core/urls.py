from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .api_views import AutomatedIncidentIngestView

urlpatterns = [
    path('', views.home, name='home'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('submit/success/', views.ticket_success, name='ticket_success'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/tickets/', views.ticket_list, name='ticket_list'),
    path('manager/tickets/<int:ticket_id>/update/', views.update_incident, name='update_incident'),

    path('unauthorized/', views.unauthorized_view, name='unauthorized'),

    # JWT Auth & API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/log-incident/', AutomatedIncidentIngestView.as_view(), name='api_log_incident'),
]
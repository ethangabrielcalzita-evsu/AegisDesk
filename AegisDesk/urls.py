from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "AegisDesk SecOps Portal"
admin.site.site_title = "AegisDesk Admin"
admin.site.index_title = "Enterprise Incident Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('incidents/', include('incident_core.urls')),
    path('', RedirectView.as_view(url='/incidents/', permanent=False)),
]

handler403 = 'incident_core.views.unauthorized_view'
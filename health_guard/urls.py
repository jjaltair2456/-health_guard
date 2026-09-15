from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('records/', include('apps.health_records.urls')),
    path('', RedirectView.as_view(url='/records/', permanent=False)),  # Redirige la raíz a /records/
]
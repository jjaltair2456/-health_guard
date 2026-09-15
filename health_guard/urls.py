from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ruta requerida para que el gráfico cargue sus scripts y datos
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    
    path('authentication/', include('apps.authentication.urls')),
    path('records/', include('apps.health_records.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('users/', include('apps.users.urls')),
]
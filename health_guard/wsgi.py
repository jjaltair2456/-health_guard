import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_guard.settings')

application = get_wsgi_application()
app = application  # Añadimos alias por compatibilidad con Vercel
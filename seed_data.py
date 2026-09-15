import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_guard.settings')
django.setup()

from apps.authentication.models import User
from apps.health_records.models import HealthRecord

def run():
    print("--- Generando datos de prueba para HealthGuard ---")

    # 1. Crear usuario pacíente de prueba
    email = "paciente@healthguard.com"
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': 'paciente_prueba',
            'first_name': 'José',
            'last_name': 'Pérez',
            'date_of_birth': '1995-06-15',
            'phone_number': '+584120000000',
        }
    )

    if created:
        user.set_password('Clave1234*')
        user.save()
        print(f"[+] Usuario creado: {email} (Contraseña: Clave1234*)")
    else:
        print(f"[*] Usando usuario existente: {email}")

    # 2. Limpiar registros previos del usuario de prueba
    HealthRecord.objects.filter(patient=user).delete()

    # 3. Generar 30 días de mediciones históricas con variaciones realistas
    now = timezone.now()
    base_weight = 76.0  # kg
    height = 175.0      # cm

    for day in range(30, 0, -1):
        record_date = now - timedelta(days=day)

        # Variaciones de los signos vitales
        weight = round(base_weight + random.uniform(-1.2, 1.2), 1)
        systolic = random.randint(112, 132)
        diastolic = random.randint(72, 86)
        heart_rate = random.randint(62, 84)
        glucose = round(random.uniform(88.0, 118.0), 1)

        record = HealthRecord.objects.create(
            patient=user,
            weight_kg=weight,
            height_cm=height,
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            heart_rate=heart_rate,
            blood_glucose=glucose,
            notes=f"Control de rutina día {31 - day}"
        )

        # Forzar la fecha histórica en la base de datos
        HealthRecord.objects.filter(id=record.id).update(recorded_at=record_date)

    print("[+] Se han generado 30 registros de salud exitosamente.")
    print("--- Proceso finalizado. Recarga el panel analítico en tu navegador. ---")

if __name__ == '__main__':
    run()
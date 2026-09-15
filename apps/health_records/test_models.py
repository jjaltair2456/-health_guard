from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.health_records.models import HealthRecord

User = get_user_model()

class HealthRecordModelTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba para asociar los registros
        self.user = User.objects.create_user(
            username='paciente_test',
            email='test@healthguard.com',
            password='securepassword123'
        )

    def test_bmi_calculation(self):
        """Verifica que el cálculo del Índice de Masa Corporal (IMC) sea correcto."""
        record = HealthRecord.objects.create(
            patient=self.user,
            weight_kg=70.0,
            height_cm=175.0,  # 1.75 m -> 1.75^2 = 3.0625 -> 70 / 3.0625 = 22.86
            systolic_bp=120,
            diastolic_bp=80,
            heart_rate=72
        )
        self.assertEqual(record.bmi, 22.86)

    def test_bp_status_normal(self):
        """Verifica que una presión arterial normal devuelva el estado adecuado."""
        record = HealthRecord.objects.create(
            patient=self.user,
            weight_kg=65.0,
            height_cm=170.0,
            systolic_bp=115,
            diastolic_bp=75,
            heart_rate=70
        )
        self.assertEqual(record.bp_status['label'], 'Normal')

    def test_bp_status_crisis(self):
        """Verifica que una presión alta se catalogue como Crisis o Etapa de riesgo."""
        record = HealthRecord.objects.create(
            patient=self.user,
            weight_kg=80.0,
            height_cm=170.0,
            systolic_bp=185,
            diastolic_bp=125,
            heart_rate=95
        )
        self.assertEqual(record.bp_status['label'], 'Crisis')

    def test_glucose_status_warning(self):
        """Verifica que niveles elevados de glucosa devuelvan la alerta correcta."""
        record = HealthRecord.objects.create(
            patient=self.user,
            weight_kg=75.0,
            height_cm=170.0,
            systolic_bp=120,
            diastolic_bp=80,
            heart_rate=75,
            blood_glucose=140.0  # Rango elevado (>= 126)
        )
        self.assertEqual(record.glucose_status['label'], 'Elevada')
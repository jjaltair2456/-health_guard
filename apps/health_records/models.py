import uuid
from django.db import models
from django.conf import settings

class HealthRecord(models.Model):
    class BloodType(models.TextChoices):
        A_POSITIVE = 'A+', 'A Positivo'
        A_NEGATIVE = 'A-', 'A Negativo'
        B_POSITIVE = 'B+', 'B Positivo'
        B_NEGATIVE = 'B-', 'B Negativo'
        O_POSITIVE = 'O+', 'O Positivo'
        O_NEGATIVE = 'O-', 'O Negativo'
        AB_POSITIVE = 'AB+', 'AB Positivo'
        AB_NEGATIVE = 'AB-', 'AB Negativo'

    # ID Único UUID (Previene IDOR y la enumeración de pacientes)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relación con el usuario del expediente
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='health_records'
    )
    
    # Datos Antropométricos y Médicos
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso (kg)")
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Estatura (cm)")
    systolic_bp = models.IntegerField(verbose_name="Presión Sistólica (mmHg)")
    diastolic_bp = models.IntegerField(verbose_name="Presión Diastólica (mmHg)")
    heart_rate = models.IntegerField(verbose_name="Frecuencia Cardíaca (BPM)")
    blood_glucose = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Glucosa en Sangre (mg/dL)")
    
    notes = models.TextField(blank=True, null=True, verbose_name="Notas de Consulta / Síntomas")
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = "Registro de Salud"
        verbose_name_plural = "Registros de Salud"

    def __str__(self):
        name = self.patient.get_full_name() or self.patient.username
        date_str = self.recorded_at.strftime('%Y-%m-%d %H:%M') if self.recorded_at else 'Reciente'
        return f"Registro {name} - {date_str}"

    @property
    def bmi(self):
        """Cálculo automático del Índice de Masa Corporal (IMC)."""
        if self.height_cm and self.height_cm > 0:
            height_m = float(self.height_cm) / 100
            return round(float(self.weight_kg) / (height_m ** 2), 2)
        return 0.0

    @property
    def bp_status(self):
        """Evalúa la categoría de la presión arterial (AHA)."""
        sys = self.systolic_bp
        dia = self.diastolic_bp

        if sys >= 180 or dia >= 120:
            return {'label': 'Crisis', 'class': 'bg-danger text-white fw-bold'}
        elif sys >= 140 or dia >= 90:
            return {'label': 'Alta (Etapa 2)', 'class': 'bg-danger text-white'}
        elif sys >= 130 or dia >= 80:
            return {'label': 'Alta (Etapa 1)', 'class': 'bg-warning text-dark'}
        elif 120 <= sys <= 129 and dia < 80:
            return {'label': 'Elevada', 'class': 'bg-info text-dark'}
        elif sys < 120 and dia < 80:
            return {'label': 'Normal', 'class': 'bg-success text-white'}
        return {'label': 'No clasificado', 'class': 'bg-secondary text-white'}

    @property
    def glucose_status(self):
        """Evalúa el nivel de glucosa en sangre (mg/dL)."""
        if self.blood_glucose is None:
            return {'label': 'No registrado', 'class': 'bg-secondary text-white'}

        g = self.blood_glucose
        if g >= 200:
            return {'label': 'Crítica', 'class': 'bg-danger text-white fw-bold'}
        elif g >= 126:
            return {'label': 'Elevada', 'class': 'bg-warning text-dark'}
        elif g < 70:
            return {'label': 'Baja (Hipoglucemia)', 'class': 'bg-danger text-white'}
        return {'label': 'Normal', 'class': 'bg-success text-white'}
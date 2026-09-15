from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    class BloodType(models.TextChoices):
        A_POSITIVE = 'A+', 'A Positivo'
        A_NEGATIVE = 'A-', 'A Negativo'
        B_POSITIVE = 'B+', 'B Positivo'
        B_NEGATIVE = 'B-', 'B Negativo'
        O_POSITIVE = 'O+', 'O Positivo'
        O_NEGATIVE = 'O-', 'O Negativo'
        AB_POSITIVE = 'AB+', 'AB Positivo'
        AB_NEGATIVE = 'AB-', 'AB Negativo'
        NOT_SPECIFIED = 'NS', 'No especificado'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices,
        default=BloodType.NOT_SPECIFIED,
        verbose_name="Tipo de Sangre"
    )
    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Estatura Base (cm)"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    emergency_contact = models.CharField(max_length=150, blank=True, null=True, verbose_name="Contacto de Emergencia")

    def __str__(self):
        return f"Perfil de {self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil cuando se registra un usuario."""
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)
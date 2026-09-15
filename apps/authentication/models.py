import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class AccessAuditLog(models.Model):
    """Capa de Auditoría: Registra accesos y modificaciones a datos sensibles."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)  # ej. "LECTURA_EXPEDIENTE", "NUEVO_REGISTRO_SALUD"
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
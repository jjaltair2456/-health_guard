from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar los datos personales básicos del usuario."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'correo@ejemplo.com'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar la información biológica base del paciente."""
    class Meta:
        model = Profile
        fields = ['birth_date', 'blood_type', 'height_cm', 'phone', 'emergency_contact']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'type': 'date'
            }),
            'blood_type': forms.Select(attrs={
                'class': 'form-select bg-dark text-white border-secondary'
            }),
            'height_cm': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'step': '0.01',
                'placeholder': '175.00'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': '+58 412 1234567'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Nombre y teléfono del contacto'
            }),
        }
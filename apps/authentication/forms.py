from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'phone_number')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none', 'placeholder': 'ejemplo@correo.com'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none', 'placeholder': '••••••••'})
    )
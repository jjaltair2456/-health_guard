from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView, FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import AccessAuditLog

def get_client_ip(request):
    """Obtiene la dirección IP real del cliente considerando proxys o balanceadores."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('authentication:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Auditoría
        AccessAuditLog.objects.create(
            user=self.object,
            action="REGISTRO_USUARIO",
            ip_address=get_client_ip(self.request)
        )
        messages.success(self.request, "Registro exitoso. Por favor inicia sesión.")
        return response

class CustomLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('analytics:dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        # Registrar auditoría de inicio de sesión exitoso
        AccessAuditLog.objects.create(
            user=user,
            action="LOGIN_EXITOSO",
            ip_address=get_client_ip(self.request)
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        # Auditoría de intenciones fallidas
        AccessAuditLog.objects.create(
            user=None,
            action="LOGIN_FALLIDO",
            ip_address=get_client_ip(self.request)
        )
        return super().form_invalid(form)

class CustomLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            AccessAuditLog.objects.create(
                user=request.user,
                action="LOGOUT",
                ip_address=get_client_ip(request)
            )
            logout(request)
        return redirect('authentication:login')
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import HealthRecord

class HealthRecordListView(LoginRequiredMixin, ListView):
    model = HealthRecord
    template_name = 'health_records/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return HealthRecord.objects.filter(patient=self.request.user).order_by('-recorded_at')

class HealthRecordDetailView(LoginRequiredMixin, DetailView):
    model = HealthRecord
    template_name = 'health_records/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return HealthRecord.objects.filter(patient=self.request.user)

class HealthRecordCreateView(LoginRequiredMixin, CreateView):
    model = HealthRecord
    fields = ['weight_kg', 'height_cm', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'blood_glucose', 'notes']
    template_name = 'health_records/create.html'
    success_url = reverse_lazy('health_records:create')

    def form_valid(self, form):
        form.instance.patient = self.request.user
        messages.success(self.request, '¡Registro de salud guardado exitosamente!')
        return super().form_valid(form)

class HealthRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = HealthRecord
    fields = ['weight_kg', 'height_cm', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'blood_glucose', 'notes']
    template_name = 'health_records/edit.html'
    success_url = reverse_lazy('health_records:list')

    def get_queryset(self):
        return HealthRecord.objects.filter(patient=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '¡Registro médico actualizado con éxito!')
        return super().form_valid(form)

class HealthRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = HealthRecord
    template_name = 'health_records/delete_confirm.html'
    success_url = reverse_lazy('health_records:list')

    def get_queryset(self):
        return HealthRecord.objects.filter(patient=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '¡Registro médico eliminado correctamente!')
        return super().delete(request, *args, **kwargs)
    
import csv
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# (Mantén tus importaciones existentes de ListView, UpdateView, DeleteView, etc.)

# --- Vistas de Exportación ---

class ExportCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expediente_medico.csv"'

        writer = csv.writer(response)
        writer.writerow(['Fecha', 'Sistolica (mmHg)', 'Diastolica (mmHg)', 'Ritmo (BPM)', 'Glucosa (mg/dL)', 'Peso (kg)', 'Notas'])

        records = HealthRecord.objects.filter(patient=request.user).order_by('-recorded_at')
        for r in records:
            writer.writerow([
                r.recorded_at.strftime('%Y-%m-%d %H:%M'),
                r.systolic_bp,
                r.diastolic_bp,
                r.heart_rate,
                r.blood_glucose,
                r.weight_kg,
                r.notes or ''
            ])

        return response


import io
import csv
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import letter as LETTER_SIZE
from reportlab.pdfgen import canvas
from .models import HealthRecord


class ExportPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        buffer = io.BytesIO()
        
        p = canvas.Canvas(buffer, pagesize=LETTER_SIZE)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 750, f"Reporte de Salud - {request.user.username}")
        
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, 720, "Fecha")
        p.drawString(150, 720, "Presión")
        p.drawString(230, 720, "Ritmo")
        p.drawString(300, 720, "Glucosa")
        p.drawString(380, 720, "Peso")

        p.line(50, 712, 550, 712)

        p.setFont("Helvetica", 10)
        y = 690
        records = HealthRecord.objects.filter(patient=request.user).order_by('-recorded_at')

        for r in records:
            if y < 50:
                p.showPage()
                y = 750

            p.drawString(50, y, r.recorded_at.strftime('%d/%m/%Y %H:%M'))
            p.drawString(150, y, f"{r.systolic_bp}/{r.diastolic_bp} mmHg")
            p.drawString(230, y, f"{r.heart_rate} BPM")
            p.drawString(300, y, f"{r.blood_glucose} mg/dL")
            p.drawString(380, y, f"{r.weight_kg} kg" if r.weight_kg else "--")
            y -= 25

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="expediente_medico.pdf"'
        return response
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.health_records.models import HealthRecord

@login_required
def dashboard_view(request):
    # Capturar rango seleccionado (por defecto 'all')
    date_range = request.GET.get('range', 'all')
    
    records = HealthRecord.objects.filter(patient=request.user).order_by('recorded_at')

    # Filtrar según el rango especificado
    now = timezone.now()
    if date_range == '7d':
        records = records.filter(recorded_at__gte=now - timedelta(days=7))
    elif date_range == '30d':
        records = records.filter(recorded_at__gte=now - timedelta(days=30))
    elif date_range == '90d':
        records = records.filter(recorded_at__gte=now - timedelta(days=90))

    total_records = records.count()
    
    # Obtener métricas generales más recientes del paciente
    all_records = HealthRecord.objects.filter(patient=request.user).order_by('recorded_at')
    latest_record = all_records.last()
    latest_bp = f"{latest_record.systolic_bp}/{latest_record.diastolic_bp}" if latest_record else "--/--"
    
    latest_bmi = "--"
    if latest_record and latest_record.weight_kg and latest_record.height_cm:
        height_m = latest_record.height_cm / 100
        latest_bmi = round(latest_record.weight_kg / (height_m ** 2), 2)

    chart_data = {
        'dates': [r.recorded_at.strftime('%d/%m %H:%M') for r in records],
        'systolic': [r.systolic_bp for r in records],
        'diastolic': [r.diastolic_bp for r in records],
        'heart_rate': [r.heart_rate for r in records],
        'glucose': [r.blood_glucose for r in records],
        'bmi': [
            round(r.weight_kg / ((r.height_cm / 100) ** 2), 2)
            if (r.weight_kg and r.height_cm) else None
            for r in records
        ]
    }

    context = {
        'total_records': total_records,
        'latest_bp': latest_bp,
        'latest_bmi': latest_bmi,
        'chart_data': chart_data,
        'selected_range': date_range,
    }
    return render(request, 'analytics/dashboard.html', context)
from django.urls import path
from .views import (
    HealthRecordListView,
    HealthRecordDetailView,
    HealthRecordCreateView,
    HealthRecordUpdateView,
    HealthRecordDeleteView,
    ExportCSVView,
    ExportPDFView,
)

app_name = 'health_records'

urlpatterns = [
    path('', HealthRecordListView.as_view(), name='list'),
    path('nuevo/', HealthRecordCreateView.as_view(), name='create'),
    path('<uuid:pk>/', HealthRecordDetailView.as_view(), name='detail'),
    path('<uuid:pk>/editar/', HealthRecordUpdateView.as_view(), name='update'),
    path('<uuid:pk>/eliminar/', HealthRecordDeleteView.as_view(), name='delete'),
    path('exportar/csv/', ExportCSVView.as_view(), name='export_csv'),
    path('exportar/pdf/', ExportPDFView.as_view(), name='export_pdf'),
]
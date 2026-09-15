from django import forms
from .models import HealthRecord

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['weight_kg', 'height_cm', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'blood_glucose', 'notes']
        widgets = {
            'weight_kg': forms.NumberInput(attrs={'step': '0.1', 'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'height_cm': forms.NumberInput(attrs={'step': '0.1', 'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'systolic_bp': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'diastolic_bp': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'blood_glucose': forms.NumberInput(attrs={'step': '0.1', 'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:border-cyan-500 focus:outline-none'}),
        }
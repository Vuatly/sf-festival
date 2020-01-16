from django import forms
from festival_app.models import Application




class CreateApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['format', 'name', 'description', 'phone', 'scene', 'performance_day', 'wishes']



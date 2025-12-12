from django import forms
from .models import Conference
class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['theme', 'name', 'location', 'start_date', 'end_date', 'description'  ]
        labels = {
            'theme': 'Conference Theme',    
            'name': 'Conference Name',
            'location': 'Location', 
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'description': 'Description',}
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':15 , 'placeholder':'Enter conference description here...'}),
        }
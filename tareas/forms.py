from django import forms
from .models import Task


class TareaForm(forms.ModelForm):
    """
    Formulario para crear una tarea
    """
    class Meta:
        """
        Clase Meta
        """
        model = Task
        fields = ['titulo', 'descripcion', 'importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la tarea'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "descripcion", "disponible"]

        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "30"}
            ),
            "autor": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "30"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "maxlength": "30"}
            ),
            "disponible": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
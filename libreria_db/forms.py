from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "descripcion", "disponible"]

        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "autor": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "disponible": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
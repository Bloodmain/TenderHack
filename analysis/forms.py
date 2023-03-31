from django import forms
from .models import Companies


class CompanyForm(forms.Form):
    @property
    def title(self):
        return "Your company"

    class Meta:
        model = Companies
        fields = ['supplier_inn']

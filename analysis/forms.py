from django import forms


class CompanyForm(forms.Form):
    inn = forms.IntegerField(label='Your inn')

    @property
    def title(self):
        return "Your company"

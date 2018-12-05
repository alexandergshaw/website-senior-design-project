from django import forms

from .models import Profile


class PhaseForm(forms.Form):
    pin1 = forms.BooleanField(required=False)
    pin2 = forms.BooleanField(required=False)
    pin3 = forms.BooleanField(required=False)
    pin4 = forms.BooleanField(required=False)
    pin5 = forms.BooleanField(required=False)
    pin6 = forms.BooleanField(required=False)
    pin7 = forms.BooleanField(required=False)
    pin8 = forms.BooleanField(required=False)
    pin9 = forms.BooleanField(required=False)
    pin10 = forms.BooleanField(required=False)
    pin11 = forms.BooleanField(required=False)
    pin12 = forms.BooleanField(required=False)
    pin13 = forms.BooleanField(required=False)
    pin14 = forms.BooleanField(required=False)
    pin15 = forms.BooleanField(required=False)
    pin16 = forms.BooleanField(required=False)


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status']

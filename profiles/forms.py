from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import password_validators_help_text_html, validate_password

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


class SetUIPasswordForm(forms.ModelForm):
    ui_password = forms.CharField(
        label='UI Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validators_help_text_html(),
    )
    ui_password_confirm = forms.CharField(
        label='Confirm UI Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = Profile
        fields = ['ui_password']

    def clean(self):
        ui_password = self.cleaned_data['ui_password']
        ui_password_confirm = self.cleaned_data['ui_password_confirm']
        if ui_password and ui_password_confirm and ui_password != ui_password_confirm:
            raise forms.ValidationError('UI Passwords do not match', code='ui_password_mismatch')
        return self.cleaned_data

    def _post_clean(self):
        super(SetUIPasswordForm, self)._post_clean()
        ui_password = self.cleaned_data['ui_password_confirm']
        if ui_password:
            try:
                validate_password(ui_password, self.instance)
            except forms.ValidationError as error:
                self.add_error('ui_password_confirm', error)

    def save(self, commit=True):
        profile = super(SetUIPasswordForm, self).save(commit=False)
        profile.ui_password = make_password(profile.ui_password)
        if commit:
            profile.save()
        return profile

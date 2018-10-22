from django import forms

choices = (
    ('less_than' , 'Less than'),
    ('equal', 'Equal'),
    ('greater_than', 'Greater Than')
)

class filterForm(forms.Form):
    date_time_cb = forms.BooleanField(required=False)
    voltage_cb = forms.BooleanField(required=False)
    current_cb = forms.BooleanField(required=False)
    power_cb = forms.BooleanField(required=False)

    date_time_select = forms.ChoiceField(choices=choices)
    voltage_select = forms.ChoiceField(choices=choices)
    current_select = forms.ChoiceField(choices=choices)
    power_select = forms.ChoiceField(choices=choices)

    date_time_tb = forms.DateTimeField(required=False)
    voltage_tb = forms.FloatField(required=False)
    current_tb = forms.FloatField(required=False)
    power_tb = forms.FloatField(required=False)
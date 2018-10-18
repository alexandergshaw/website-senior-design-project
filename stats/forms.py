from django import forms

choices = (
    ('less_than' , 'Less than'),
    ('equal', 'Equal'),
    ('greater_than', 'Greater Than')
)

class filterForm(forms.Form):
    date_time_cb = forms.BooleanField()
    voltage_cb = forms.BooleanField()
    current_cb = forms.BooleanField()
    power_cb = forms.BooleanField()

    date_time_select = forms.ChoiceField(choices=choices)
    voltage_select = forms.ChoiceField(choices=choices)
    current_select = forms.ChoiceField(choices=choices)
    power_select = forms.ChoiceField(choices=choices)

    date_time_tb = forms.DateTimeField()
    voltage_tb = forms.FloatField()
    current_tb = forms.FloatField()
    power_tb = forms.FloatField()
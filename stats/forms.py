from django import forms
from django.forms.widgets import SelectDateWidget
import datetime

choices = (
    ('less_than' , 'Less than'),
    ('equal', 'Equal'),
    ('greater_than', 'Greater Than')
)

current_year = datetime.datetime.now().year
years = []
for i in range(2015, current_year):
    years.append(str(i))
years.append(str(current_year))

class filterForm(forms.Form):
    date_time_cb = forms.BooleanField(required=False)
    voltage_cb = forms.BooleanField(required=False)
    current_cb = forms.BooleanField(required=False)
    power_cb = forms.BooleanField(required=False)

    date_time_select = forms.ChoiceField(choices=(('before', 'Before'), ('after', 'After')))
    voltage_select = forms.ChoiceField(choices=choices)
    current_select = forms.ChoiceField(choices=choices)
    power_select = forms.ChoiceField(choices=choices)

    date_time_tb = forms.DateTimeField(required=True, widget=SelectDateWidget(
        # empty_label=("Choose Year", "Choose Month", "Choose Day"),
        # empty_label=''
        years=years
    ))
    voltage_tb = forms.FloatField(required=False)
    current_tb = forms.FloatField(required=False)
    power_tb = forms.FloatField(required=False)
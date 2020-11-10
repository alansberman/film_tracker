from django import forms
from django.forms import ModelForm
from .models import Show


class ShowSearchForm(forms.Form):
    search_query = forms.CharField(label='Show Title', max_length=100)


class ShowForm(ModelForm):
    class Meta:
        model = Show
        fields = ['score', 'comments', 'date_watched']  # , 'date_watched'
        # Thanks to https: // stackoverflow.com/questions/49440853/django-2-0-modelform-datefield-not-displaying-as-a-widget
        widgets = {
            'date_watched': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }

from django import forms
from django.core.exceptions import ValidationError
from .models import User



class RatingForm(forms.Form):
    value = forms.IntegerField(
        label='امتیاز',
        min_value=1,
        max_value=5,
    )
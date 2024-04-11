from django import forms
from requests import Response

from comment.models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "توضیحات"}),
        }
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response_Comment
        fields = ['response']

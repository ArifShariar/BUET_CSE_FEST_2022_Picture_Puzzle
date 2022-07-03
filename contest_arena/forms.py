from django import forms

from .models import *


class PuzzleAnsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PuzzleAnsForm, self).__init__(*args, **kwargs)
        self.fields['ans'] = forms.CharField(widget=forms.TextInput, max_length=40)
        self.fields['ans'].widget.attrs = {'class': 'form-control', 'placeholder': 'Puzzle Answer',
                                           'required': 'required'}

    class Meta:
        model = PuzzleForm
        fields = ('ans',)

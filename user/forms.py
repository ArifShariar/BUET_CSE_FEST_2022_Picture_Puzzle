from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

ACC_TYPE = (
    (1, "Alumni"),
    (2, "Current Student"),
)


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'User Handle',
                                                'required': 'required'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email',
                                             'required': 'required'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password',
                                                 'required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm Password',
                                                 'required': 'required'}

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ParticipantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)

        self.fields['acc_type'] = forms.ChoiceField(choices=ACC_TYPE)
        self.fields['acc_type'].widget.attrs = {'class': 'form-control', 'required': 'required'}

        self.fields['student_ID'].widget.attrs = {'class': 'form-control', 'required': 'required',
                                                  'placeholder': 'Student Id'}

    class Meta:
        model = Participant
        fields = ('acc_type', 'student_ID')

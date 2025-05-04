from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Loan

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoanForm(forms.ModelForm):
    loan_period = forms.ChoiceField(
        choices=[(7, '1 viikko'), (14, '2 viikkoa'), (21, '3 viikkoa'), (28, '4 viikkoa')],
        initial=14,
        label="Laina-aika (päivinä)"
    )



class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = []

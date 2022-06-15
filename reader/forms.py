from django import forms
from .models import reader,contact_us

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ReaderRegisterForm(UserCreationForm):
    # username = forms
    email = forms.EmailField(max_length=120,help_text="Please input a valid email.")
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = "__all__"
from django import forms
from books.models import book,shells

class shell_form(forms.ModelForm):
    class Meta:
        model = shells
        fields = ['name','upload_by']

__author__ = 'phillip'
from django import forms

class SignUpForm(forms.Form):

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(max_length=50, required=True)
    password_confirmation = forms.CharField(max_length=50, required=True)
    reCaptcha = forms.CharField(max_length=20, required=True)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        if cleaned_data.password != cleaned_data.password_confirmation:
            raise forms.ValidationError("Passwords are not the same.")

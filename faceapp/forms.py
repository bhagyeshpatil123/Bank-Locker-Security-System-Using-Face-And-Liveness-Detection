from django import forms
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=30, label="Login Email")
    password = forms.CharField(max_length=30, min_length=3, widget=forms.PasswordInput, label='Login Password')

class UserRegisterForm(UserLoginForm):
    name = forms.CharField(max_length=30, min_length=2, label="User Name")
    mobile = forms.CharField(label="User Mobile", help_text="Country code is mandatory(eg. +91XxXxXxXxXx)", validators=[])
    address = forms.CharField(max_length=99, min_length=2, label="User Address", widget=forms.Textarea)

    def clean_mobile(self):
        mobile=self.cleaned_data.get('mobile')
        try:
            pass
        except Exception as ex:
            pass

        #https://stackoverflow.com/questions/52322148/django-validate-password-with-auth-password-validators/52336995
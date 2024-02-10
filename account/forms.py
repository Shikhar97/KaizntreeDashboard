from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'shadow form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'shadow form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'shadow-sm form-control', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set help_text to an empty string for each field
        for field_name, field in self.fields.items():
            field.help_text = None

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'shadow form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'shadow form-control', 'placeholder': 'Password'}))
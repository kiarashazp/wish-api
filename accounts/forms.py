from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] and cd['confirm_password'] and cd['password'] != cd['confirm_password']:
            raise ValidationError('passwords don\'t match')
        return cd['confirm_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can't change password user by this form")

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'last_login')

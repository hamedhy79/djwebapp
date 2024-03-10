from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForms(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Username'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}))
    password2 = forms.CharField(
        label='Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your confirm Password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError(_("این نام کاربری از قبل وجود دارد"))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError(_("این ایمیل از قبل وجود دارد"))
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')
        if p1 and p2 and p2 != p1:
            raise ValidationError("رمز های عبور باید باهم برابر باشند")


# login
class UserLoginForms(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Password'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age', 'bio',)

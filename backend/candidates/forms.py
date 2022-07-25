from django import forms
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username=forms.CharField(label='username', max_length=200)
    password=forms.CharField(label='password', max_length=200)
    class Meta:

        model = Profile      
 
        fields =["username", "password"]

    def clean(self):

        super(LoginForm, self).clean()
         
        username_field = self.cleaned_data.get('username')

        if not username_field or not User.objects.get(username=username_field):
            self.add_error('username', 'incorrect username or password')

        return self.cleaned_data

class RegisterForm(forms.Form):
    username=forms.CharField(label='username', max_length=200)
    password=forms.CharField(label='password', max_length=200)
    email=forms.CharField(label='email', max_length=200)
    password1=forms.CharField(label='password1', max_length=200)

    class Meta:

        model = Profile      
 
        fields =["username", "password", "email", "password1"]

    def clean(self):

        super(RegisterForm, self).clean()
         
        username_field = self.cleaned_data.get('username')
        password_field = self.cleaned_data.get('password')
        password1_field = self.cleaned_data.get('password1')
        email_field = self.cleaned_data.get('email')

        if email_field:
            try:
                validate_email(email_field)
            except ValidationError:
                self.add_error('email', 'incorrect email')

        if password1_field != password_field:
            self.add_error('password1', "doesn't match")

        if password_field:
            try:
                validate_password(password_field)
            except ValidationError:
                self.add_error('password', 'incorrect password')

        if username_field:
            try:
                User.objects.get(username=username_field)
                self.add_error('username', 'username already exists')
            except:
                pass

        return self.cleaned_data
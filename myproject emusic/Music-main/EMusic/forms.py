# EMusic/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        help_text='Enter a valid email address',
        error_messages={
            'invalid': 'Please enter a valid email address.',
            'required': 'Email address is required.',
        }
    )
    first_name = forms.CharField(
        max_length=100, 
        error_messages={'required': 'First name is required.'}
    )
    last_name = forms.CharField(
        max_length=100, 
        error_messages={'required': 'Last name is required.'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        error_messages = {
            'username': {
                'required': 'This field is required.',
                'unique': 'This username is already taken.',
            },
            'password1': {
                'required': 'Please enter a password.',
            },
            'password2': {
                'required': 'Please confirm your password.',
                'mismatch': 'The two password fields don’t match.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email




class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




from django.contrib.auth.forms import PasswordChangeForm
from .models import ProfileSettings
from django.contrib.auth.models import User

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = ProfileSettings
        fields = ['bio', 'location', 'profile_photo']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



from .models import SongUpload

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = SongUpload
        fields = ['audio_file']
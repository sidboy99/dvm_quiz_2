from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

'''
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
'''


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=Profile.choices)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1', 'password2', 'user_type']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        profile = Profile.objects.get(user=user)
        profile.user_type = self.cleaned_data['user_type']
        profile.save()
        return profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo', )

class FollowUsersForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('follows',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the currently logged-in user from the list
        self.fields['follows'].queryset = User.objects.exclude(pk=self.instance.pk)
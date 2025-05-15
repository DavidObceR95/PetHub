from django.forms import ModelForm, CharField, PasswordInput
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class createcitasform(ModelForm):
    class Meta:
        model =  Appointment
        fields = ['petname', 'description']


class CreateCustomUser(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'first_name', 'last_name', 'password', 'phone', 'role']

class CreateCustomPublicUser(ModelForm):
    password1 = CharField(widget=PasswordInput, label='Repeat Password') 
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password1', 'phone', 'role']

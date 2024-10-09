from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Bill, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'national_id', 'email', 'password1', 'password2']


class BillForm(ModelForm):
    class Meta:
        model = Bill 
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'national_id','phone_no']

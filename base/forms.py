from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm

# creating a model form based on the model room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        # gives all the fields of model room.
        fields = '__all__'
        exclude = ['host','participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','avatar','bio','username','email']

# new user creation form.
class MyUSerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']
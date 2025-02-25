from django.forms import ModelForm
from .models import Room
# to make user edit forms.
from django.contrib.auth.models import User

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
        fields = ['username','email']
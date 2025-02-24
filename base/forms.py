from django.forms import ModelForm
from .models import Room

# creating a model form based on the model room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        # gives all the fields of model room.
        fields = '__all__'
        exclude = ['host','participants']
from django.contrib import admin

# Register your models here.
from .models import Room,Message,Topic,User
# initially we did not have to import the User model because it was inbuilt but now we are using custom user model thus we need to register it.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(User)
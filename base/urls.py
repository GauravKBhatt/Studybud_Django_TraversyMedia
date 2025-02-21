from django.urls import path
from . import views

urlpatterns = [
    # this is to make sure that the website first lands on the home page.
    path('',views.home,name="Home"),
    # this is to make sure the home link from navbar routes to the home page
    path('home',views.home,name="Home"),
    # now we need to make sure this allows dynamic routing so, that we can go to different rooms by passing the value in the parameter.Although we will be passing an integer in place of pk, we are assigning str for increased flexibility. 
    path('room/<str:pk>/',views.room,name="Room"),

    # url for creating a new room
    path('create-room/',views.createRoom, name="create-room"),
    # url for updating an existing room
    path('update-room/<str:pk>',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>',views.deleteRoom,name="delete-room")
    ]
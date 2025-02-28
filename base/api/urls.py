from django.urls import path
from . import views

urlpatterns =[
    # for uri: http/api etc.
    path('',views.getRoutes),
    path('rooms/',views.getRooms),
    path('rooms/<str:pk>/',views.getRoom)
]
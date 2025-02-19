from django.shortcuts import render
from django.http import HttpResponse

#using the HttpResponse method.
# def home(request):
#     return HttpResponse('Home Page')
# def room(request):
#     return HttpResponse('Room')

# creating a list of roots that will be rendered in the home template
rooms=[
    {'id':1,'name':"Python"},
    {'id':2,'name':"Django"},
    {'id':3,'name':"javascript"},
]

# using the render method.
def home(request):
    # creating a dictionary out of the list room
    context={'rooms':rooms}
    return render(request,'base/home.html',context)
def room(request):
    return render(request,'base/room.html')
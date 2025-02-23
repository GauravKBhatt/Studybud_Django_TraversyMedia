from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# this helps us add AND OR to the queries
from .models import Room,Topic
from django.db.models import Q
from django.contrib import messages 
from django.contrib.auth import authenticate, login,logout
# importing a drecorator to restrict some pages for some users.
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
# importing the inbuilt user signup form from django
from django.contrib.auth.forms import UserCreationForm
#using the HttpResponse method.
# def home(request):
#     return HttpResponse('Home Page')
# def room(request):
#     return HttpResponse('Room')

# creating a list of roots that will be rendered in the home template.OVERRIDED BY THE QUERY LATER ON
# rooms=[
#     {'id':1,'name':"Python"},
#     {'id':2,'name':"Django"},
#     {'id':3,'name':"javascript"},
# ]

def loginPage(request):
    # to identify if the logic is for login or regidter
    page='login'
    # if i am logged in already, I should not be allowed to even be on this page.
    if request.user.is_authenticated:
        redirect('Home')
    if request.method =='POST':
        # add .lower() later but now Gaurav and Tim are in uppercase in the DB
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'The password does not match with the username.')
        except User.DoesNotExist:
            messages.error(request, 'The user does not exist.')
    context={'page':page}
    return render(request,'base/login_register.html',context)

# figuring out logout
def logoutPage(request):
    logout(request)
    return redirect('Home')

# register
def registerPage(request):
    page='register'
    form = UserCreationForm()
    context = {'page':page,'form':form}
    form=UserCreationForm(request.POST)
    if form.is_valid():
        # first we want to clean the data like making sure all the usenrame characters are in lower case, thus, we do not commit immediately.
        user=form.save(commit=False)
        user.username=user.username.lower()
        user.save()
        login(request,user)
        return redirect('Home')
    else:
        messages.error(request,"Some error occured during the registration process.")
    return render(request,'base/login_register.html',context)
# using the render method.
def home(request):
    if request.GET.get('q')!=None:
        q=request.GET.get('q')
    else:
        q=''
    # We are no more using the data specified in this file. We now use the data in the database through queries.
    # rooms = Room.objects.all() this is commented out because now we will query the room through filter method showing only those rooms as searched by the user.
    topics = Topic.objects.all()
    # topic is a different model thus, we need to specify the model name too, rest are the attributes of the room model.
    rooms =Room.objects.filter (Q(topic__name__icontains=q) | Q(name__icontains='q') | Q(description__icontains='q'))
    room_count=rooms.count() 
    # creating a dictiory out of the list room
    context={'rooms':rooms,'topics':topics,'room_count':room_count}

    return render(request,'base/home.html',context)
# passing another pk parameter that was defined in the urls.py for dynamic routing. 
def room(request,pk):
    # query into the database gets the exact room we are looking for.
    room=Room.objects.get(id=pk)
    # code to identify the room that correlates to the parameter pk. NOT NEEDED AFTER THE QUERY
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    context ={'room':room}
    # returning the room that matches with the parameter pk
    return render(request,'base/room.html',context)

# redirecting a user to the login page to create a room if the user is not logged in properly
@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        # instead of individually isolating the 'name' etc, request.post takes care of all at once.
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context ={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    # makes sure the update form is prefilled with the information.
    form = RoomForm(instance=room)
    # to make sure only the host of the room can edit the room. 
    if request.user != room.host:
        return HttpResponse("You are not the host of this room.Thus, you cannot edit it.")
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)

# logic to delete the room 
@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('Home')
    return render(request,'base/delete.html',{'obj':room})
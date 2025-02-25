from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# this helps us add AND OR to the queries
from .models import Room,Topic,Message
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
    rooms =Room.objects.filter (Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    room_count=rooms.count() 
    # this makes sure to display only the messages of the room you are in the recent activity feed.
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    # creating a dictiory out of the list room
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}

    return render(request,'base/home.html',context)
# passing another pk parameter that was defined in the urls.py for dynamic routing. 
def room(request,pk):
    # query into the database gets the exact room we are looking for.
    room=Room.objects.get(id=pk)
    # all the child components of the room.
    room_messages=room.message_set.all()
    participants=room.participants.all()
    # code to identify the room that correlates to the parameter pk. NOT NEEDED AFTER THE QUERY
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room=i
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room
        )
        room.participants.add(request.user)
        return redirect('Room',pk=room.id)
    context ={'room':room,'room_messages':room_messages,'participants':participants}
    # returning the room that matches with the parameter pk
    return render(request,'base/room.html',context)

# redirecting a user to the login page to create a room if the user is not logged in properly
@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        # instead of individually isolating the 'name' etc, request.post takes care of all at once.
        # for the create room form.
        topic_name = request.POST.get('topic')
        # if the get does not get the object with certain name then the created will be 1 otherwise 0.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # new way of creating the object. The old way is commented below.
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     # to make sure that the host name is dynamically added to the form.
        #     room = form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('Home')
    context ={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='loginPage')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    # makes sure the update form is prefilled with the information.
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # to make sure only the host of the room can edit the room. 
    if request.user != room.host:
        return HttpResponse("You are not the host of this room.Thus, you cannot edit it.")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        # we will get that newly created or existing.
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('Home')
    context={'form':form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html',context)

# logic to delete the room 
@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not the host of this room.Thus, you cannot delete it.")
    if request.method=='POST':
        room.delete()
        return redirect('Home')
    return render(request,'base/delete.html',{'obj':room})

# logic to delete the message 
@login_required(login_url='loginPage')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not the owner of this message.Thus, you cannot edit it.")
    if request.method=='POST':
        message.delete()
        return redirect('Home')
    return render(request,'base/delete.html',{'obj':message})

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)
from django.contrib.auth import authenticate,login,logout

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import RoomForm, userForm,MyUserCreationForm
from django.contrib import messages

# Create your views here.

#rooms = [
  #  {'id':1, 'name':'Lets learn python!'},
  #  {'id':2, 'name':'Django!'},
 #   {'id':3, 'name':'Backend devs!'},
#]

def loginPage(request):
    page = 'login'
    user = None  # Initialize the user variable

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    context = {'form':form}

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration.")
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | #or
                                Q(name__icontains=q) |
                                Q(description__contains=q))

    #icontains means if we only write py instead of python, it will still try to detect

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
#    for i in rooms:
#        if i['id'] == int(pk):
#           room = i
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room = Room(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        try:
            room.save()
            return redirect('home')
        except IntegrityError as e:
            # Handle the integrity error, e.g., duplicate room name
            form.add_error(None, 'An error occurred: {}'.format(str(e)))

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #pre-fill the existing data

    if request.user != room.host: #cant update others' room
        return HttpResponse('Get out!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = request.POST.get('topic')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Get out!')

    if request.method == 'POST': #post means we clicked confirm
        room.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Get out!')

    if request.method == 'POST': #post means we clicked confirm
        message.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = userForm(instance=user)

    if request.method == "POST":
        form = userForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)
    return render(request,'base/update-user.html',{'form':form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
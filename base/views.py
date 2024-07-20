from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib import messages
# Create your views here.

#rooms = [
  #  {'id':1, 'name':'Lets learn python!'},
  #  {'id':2, 'name':'Django!'},
 #   {'id':3, 'name':'Backend devs!'},
#]

def loginPage(request):
    user = None  # Initialize the user variable
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")

    context = {}
    return render(request, 'base/login_register.html', context)

    context={}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | #or
                                Q(name__icontains=q) |
                                Q(description__contains=q))

    #icontains means if we only write py instead of python, it will still try to detect

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics, 'room_count':room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
#    for i in rooms:
#        if i['id'] == int(pk):
#           room = i
    context = {'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
       form = RoomForm(request.POST)
       if form.is_valid():
            form.save() #save it in database
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #pre-fill the existing data

    if request.method == "POST":
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST': #post means we clicked confirm
        room.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':room})


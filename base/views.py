from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.

#rooms = [
  #  {'id':1, 'name':'Lets learn python!'},
  #  {'id':2, 'name':'Django!'},
 #   {'id':3, 'name':'Backend devs!'},
#]
def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
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
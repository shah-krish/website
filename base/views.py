from django.shortcuts import render
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
    context = {'form':form}
    return render(request,'base/room_form.html',context)


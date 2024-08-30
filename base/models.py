from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null = True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):

    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null = True) #wont delete room if topic is deleted
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank= True) #can be blank
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True) #each time save is called, take time stamp
    created = models.DateTimeField(auto_now_add=True) #only takes time stamp when first instance created

    class Meta:
        ordering = ['-updated','-created'] #- means descending

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) #each message has 1 user
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #when room is deleted, all children(msg) are deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','-created'] #- means descending
    def __str__(self):
        return self.body[0:50] #only first 50 characters displayed to avoid clutter


from django.db import models
from account.models import User

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(User)
    description = models.CharField(max_length=50, default="")

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
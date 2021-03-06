from django.db import models
from account.models import User

# Create your models here.
class Calendar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
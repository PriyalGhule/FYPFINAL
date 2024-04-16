from django.db import models
from django.contrib.auth.models import User



class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    phone=models.BigIntegerField(max_length=50,null=True)
    role=models.CharField(max_length=50)



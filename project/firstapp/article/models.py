from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
###
from django.contrib.auth.models import AbstractBaseUser
###
from django.contrib.auth.models import UserManager

# Create your models here.

'''
Класс Author описывает новую модель таблицы, включающие все поля регистрации пользователя (Отказался от стандартной таблицы Django)
'''
class Author(models.Model):
    #id = models.CharField(primary_key=False, max_length=128)
    #last_login = models.IntegerField(max_length=2)
    username = models.CharField(unique=True,  max_length=128)
    email = models.CharField(primary_key=True, max_length=128)
    age = models.IntegerField(max_length=2)
    password = models.CharField(max_length=128)

    gender = models.CharField(max_length=10)
    #is_active = models.BooleanField(null=True)
    #last_login = models.IntegerField(max_length=2)
    #USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['password']
    #objects = UserManager()
    def __str__(self):
        return self.username


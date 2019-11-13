from django.db import models

class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32)
    c_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Invita(models.Model):
    name = models.CharField(max_length=32)
    invitacode = models.CharField(max_length=6,unique=True)
    invitaname = models.CharField(max_length=32,null=True)

    def __str__(self):
        return self.name
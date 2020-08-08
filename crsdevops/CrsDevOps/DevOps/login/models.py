from django.db import models

class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32)
    admin = models.CharField(max_length=2)
    CreateTime = models.CharField(max_length=20,null=True)


    def __str__(self):
        return self.name

class Invita(models.Model):
    name = models.CharField(max_length=32)
    invitacode = models.CharField(max_length=6,unique=True)
    invitavercode = models.CharField(max_length=6,null=True)
    invitaname = models.CharField(max_length=32,null=True)

    def __str__(self):
        return self.name

class VerCode(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=6, unique=True)
    recode = models.CharField(max_length=6,null=True)

    def __str__(self):
        return self.name

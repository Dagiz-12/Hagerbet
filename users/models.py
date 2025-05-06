from django.db import models


class Users(models.Model):
    fname = models.CharField(max_length=128)
    lname = models.CharField(max_length=128)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)

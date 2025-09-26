from django.db import models

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
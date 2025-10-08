from django.db import models

# Create your models here.
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=20)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    unit = models.CharField(max_length=5)
    price = models.FloatField(default=0.0)
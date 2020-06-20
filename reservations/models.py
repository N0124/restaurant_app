from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()


class Table(models.Model):
    max_capacity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    shape = models.CharField(max_length=25, choices=(('rectangular', 'rectangular'), ('oval', 'oval')))
    coordinates = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    size = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])


class Reservation(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tables = models.ManyToManyField(Table)

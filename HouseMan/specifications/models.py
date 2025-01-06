from django.db import models


# Create your models here.

class Address(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(unique=True)
    street = models.CharField(max_length=50)
    building_num = models.CharField(max_length=7)
    korp = models.CharField(max_length=3)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Address"

class Building(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    number_of_floors = models.CharField(max_length=10)
    number_of_entrances = models.IntegerField()
    number_of_elevators = models.IntegerField()
    number_of_chutes = models.IntegerField()
    number_of_residents = models.IntegerField()
    number_of_entrances = models.IntegerField()
    cleaning_area = models.DecimalField(max_digits=10, decimal_places=2)
    residential_area = models.DecimalField(max_digits=10, decimal_places=2)

from django.db import models


# Create your models here.

class Address(models.Model):
    title = models.CharField(unique=True)
    street = models.CharField(max_length=50)
    building_num = models.CharField(max_length=7)
    korp = models.CharField(max_length=3)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Address"

class Building(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    number_of_floors = models.CharField(max_length=10)
    number_of_entrances = models.IntegerField()
    number_of_elevators = models.IntegerField()
    number_of_chutes = models.IntegerField()
    number_of_residents = models.IntegerField()
    cleaning_area = models.DecimalField(max_digits=10, decimal_places=2)
    residential_area = models.DecimalField(max_digits=10, decimal_places=2)


class Unit(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

#        class Meta:
#            managed = False
#            db_table = 'specifications_unit'

#            db_table_comment = 'Units of measurement'

'''
Building.objects.create(id = 2, title='Задонский пр., д.16, к.1',
                        address_id=2, number_of_floors = 12, number_of_entrances = 8,
                        number_of_elevators=16, number_of_chutes=8, number_of_residents=1083,
                        cleaning_area=1007, residential_area=12934.6)
Building.objects.create(id = 3, title='Кустанайская ул., д.10, к.1',
                        address_id=4, number_of_floors = 9, number_of_entrances = 8,
                        number_of_elevators=8, number_of_chutes=8, number_of_residents=918,
                        cleaning_area=1029.1, residential_area=13490.2)
'''

from django.db import models

# Create your models here.

class Address(models.Model):
    title = models.CharField(unique=True, max_length=70)
    street = models.CharField(max_length=50)
    building_num = models.CharField(max_length=7)
    korp = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Address"

class Building(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True)
    number_of_floors = models.CharField(max_length=10, blank=True)
    number_of_entrances = models.IntegerField(blank=True)
    number_of_elevators = models.IntegerField(blank=True)
    number_of_chutes = models.IntegerField(blank=True)
    number_of_residents = models.IntegerField(blank=True)
    cleaning_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    residential_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True)



class Unit(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

#        class Meta:
#            managed = False
#            db_table = 'specifications_unit'
#            db_table_comment = 'Units of measurement'


class ExpenseItem(models.Model):
    title = models.CharField(unique=True, max_length=70)
    sort_num = models.IntegerField(default=0)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["sort_num"]

class Expenses(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='expenses' )
    item = models.ForeignKey(ExpenseItem, on_delete=models.PROTECT, related_name='building_expenses')
    summ = models.DecimalField(max_digits=12, decimal_places=2, default = 0.0)
    type = models.CharField(max_length=5, default='месяц')
    def __str__(self):
        return f'{self.building} _ {self.item}: {self.summ} руб. в {self.type}'

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

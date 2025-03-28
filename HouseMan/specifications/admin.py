from django.contrib import admin
from .models import Building, ExpenseItem, Expenses


# Register your models here.
'''
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('street',)
    list_per_page = 30
'''
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('number_of_floors', 'number_of_entrances', 'number_of_elevators', 'number_of_residents')
    list_per_page = 30

@admin.register(ExpenseItem)
class ExpItemAdmin(admin.ModelAdmin):
    list_display = ('sort_num', 'title')
    search_fields = ('title',)
    list_per_page = 40

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('building', 'item', 'summ', 'type')
    search_fields = ('building', 'item',)
    list_filter = ('building', 'item',)
    list_per_page = 40

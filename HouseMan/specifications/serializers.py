from rest_framework import serializers
from .models import Address, Building

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('title', 'street', 'building_num', 'korp')

class AddressModel:
    def __init__(self,title):
        self.title = title

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('title', 'street', 'building_num', 'korp')

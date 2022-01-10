from django.db.models import fields
from rest_framework import serializers
from .models import *

class CarsSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Cars
        fields = '__all__'

class AvgratingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Avgrating
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):


    class Meta:
        model = Rating
        fields = '__all__'
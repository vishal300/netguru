import datetime
import os
from typing import ClassVar, final
from django.core.checks import messages
from django.db.models.aggregates import Avg
from django.db.models.query import Prefetch
from django.utils import timezone
from requests.api import delete
from rest_framework import generics, status
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import Response
from django.core.serializers import serialize
from django.db.models import Count,  F
from .serializers import *
from .models import *
import json
import time
import requests,json



class CarsApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset  = Cars.objects.filter(status__gt=0)
    serializer_class = CarsSerializer
    
    def get(self,request,car_id=None):
        car_obj=Cars.objects.all().prefetch_related(
                                                'avg'
                                        )
        car_obj = car_obj.values(
                                    'make','model'
                            ).annotate(
                                avg_rating =F('avg__avg_rating')
                            )
        return Response(car_obj)

    def post(self,request,car_id=None):
        import pdb; pdb.set_trace()
        if request.data:
            try:
                car_make = request.data.get('make')
                car_model = request.data.get('model')
                #,'model':car_model
                data ={'Make_Name':car_make,'Model_Name':car_model}
                url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/'+car_make+'?format=json'
                post_fields = {'format': 'json', 'data':data}
                headers = {
                            'Content-Type': "application/x-www-form-urlencoded",
                            'cache-control': "no-cache" 
                        } 
                result = requests.request("GET", url, data=data, headers=headers)
                if result.status_code == 200:
                    response_data = result.json()['Results']
                    if response_data:
                        for fe in response_data:
                            if fe['Make_Name'].upper() == car_make.upper() and fe['Model_Name'].upper() == car_model.upper():
                                car_obj = Cars.objects.filter(
                                                                make = car_make,
                                                                model = car_model
                                                            )
                                if car_obj:
                                    return Response('Data Already present in the DataBase')
                                serializer = CarsSerializer(data=request.data)
                                if serializer.is_valid():
                                    serializer.save()
                                    return Response(serializer.data,
                                                        status=status.HTTP_201_CREATED)
                                return Response(serializer.errors, 
                                                        status=status.HTTP_400_BAD_REQUEST)
                            else:
                                pass
                            message = "Car and Model is not present in API"
                            return Response(message)
                    else:
                        message = "Return Nothing"
                        return Response(message)
                else:
                    return Response(result.text())
            except Exception as e:
                return Response(
                                    e,status=status.HTTP_400_BAD_REQUEST
                                )
    
    def delete(self,request,car_id=None):
        if car_id:
            car_obj = Cars.objects.filter(
                                            car_id=car_id
                                        )
            if car_obj:
                car_obj.delete()
                message = "Delete Successfuly"
                return Response(message,status=status.HTTP_200_OK)
            else:
                message = "No car is Present in DataBase"
                return Response(message)
        else:
            message = "Please pass the ID in url"
            return Response(message)
        
        
class CarsPopularApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset  = Avgrating.objects.filter(status__gt=0)
    serializer_class = AvgratingSerializer

    def get(self,request):
        pop_obj = Cars.objects.all().prefetch_related(
                                                'avg_rating'
                                        )
                                        
        pop_obj = pop_obj.values(
                                    'make', 'model'
                            ).annotate(
                                          rates_number=Count('avg_rating__rating')
                                    )
        return Response(pop_obj)


class RatingApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset  = Avgrating.objects.filter(status__gt=0)
    serializer_class = AvgratingSerializer

    def get(self,request):
        rating_obj = Rating.objects.filter(status__lte=0)
        return Response(rating_obj,
                                    status=status.HTTP_200_OK)

    def post(self,request):
        if request.data:
            data = request.data
            rating = data['avg_rating']
            car_id = data['car_id']
            s_data = {'car_id':car_id,'status':1}
            averagerating = self.averagerating(s_data)
            final_data = {
                            'car_id': car_id,
                            'avg_rate_id': averagerating,
                            'rating': rating,
                            'status':1
                        }
            rating_serializer = RatingSerializer(data = final_data)
            if rating_serializer.is_valid():
                rating_serializer.save()
                avg_obj = Rating.objects.filter(
                                                    car_id=car_id,avg_rate_id=averagerating
                                                ).aggregate(Avg('rating'))
                avg_rating = Avgrating.objects.filter(
                                                        car_id=car_id,avg_rate_id=averagerating
                                                    ).update(
                                                        avg_rating=avg_obj['rating__avg']
                                                            )
                return Response(avg_rating,
                                             status=status.HTTP_201_CREATED)
                
            return Response(rating_serializer.errors, 
                                            status=status.HTTP_400_BAD_REQUEST)
            
        return Response([],
                            status=status.HTTP_201_CREATED)


    def averagerating(self,data):
        car_id  = data['car_id']
        avg_obj = Avgrating.objects.filter(car_id=car_id).values('avg_rate_id')
        if avg_obj:
            avg_id = avg_obj[0]['avg_rate_id']
            return avg_id
        else:
            avg_serializer = AvgratingSerializer(data = data)
            if avg_serializer.is_valid():
                avg_serializer.save()
                avg_id = avg_serializer.data['avg_rate_id']
            return avg_id
        




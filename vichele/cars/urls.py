from django.urls import path
from . import views
from django.conf import settings
from .views import *
urlpatterns = [
    path('cars/<int:car_id>',CarsApiView.as_view(),name = 'car-list'),
    path('cars/',CarsApiView.as_view(),name = 'car-list'),
    path('popular/',CarsPopularApiView.as_view(),name = 'pop-list'),
    path('rate/',RatingApiView.as_view(),name = 'rate-list'),
]
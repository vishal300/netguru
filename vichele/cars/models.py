from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Cars(models.Model):
    car_id = models.AutoField(primary_key=True)
    make = models.CharField(
                                max_length=255
                            )
    model = models.CharField(
                                max_length=255
                            )
    status = models.PositiveIntegerField(default=1)


class Avgrating(models.Model):
    car_id = models.ForeignKey(
                                Cars,
                                on_delete=models.CASCADE,
                                related_name="avg"
                            )
    avg_rate_id = models.AutoField(primary_key = True)
    avg_rating = models.FloatField(null=True,blank=True,validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    status = models.PositiveIntegerField(default=1)

    # def __str__(self):
    #     return self.avg_rate_id


class Rating(models.Model):

    avg_rate_id = models.ForeignKey(
                                        Avgrating,
                                        on_delete=models.CASCADE,
                                        related_name="rating"
                                    )
    car_id = models.ForeignKey(
                                Cars,
                                on_delete=models.CASCADE,
                                related_name="avg_rating"
                            )
    rate_id = models.AutoField(primary_key=True)
    rating = models.FloatField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    status = models.PositiveIntegerField(default=1)
    
    # def __str__(self):
    #     return self.rate_id
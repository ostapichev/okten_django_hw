from django.db import models

from core.models import BaseModel


class CarModel(BaseModel):
    brand = models.CharField(max_length=25)
    price = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        db_table = 'cars'

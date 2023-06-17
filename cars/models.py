from django.db import models


class CarModel(models.Model):
    brand = models.CharField(max_length=25)
    price = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        db_table = 'cars'

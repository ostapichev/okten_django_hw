from django.db import models


class CarModel(models.Model):
    brand = models.CharField(max_length=25)
    year = models.IntegerField()
    num_seats = models.IntegerField()
    body_type = models.CharField(max_length=15)
    engine_volume = models.FloatField()

    class Meta:
        db_table = 'cars'

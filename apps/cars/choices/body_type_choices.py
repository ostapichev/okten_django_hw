from django.db import models


class BodyTypeChoices(models.TextChoices):
    hatchback = 'Hatchback'
    sedan = 'Sedan'
    muv_suv = 'MUV / SUV'
    coupe = 'Coupe'
    convertible = 'Convertible'
    wagon = 'Wagon'
    van = 'Van'
    jeep = 'Jeep'

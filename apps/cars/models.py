from datetime import datetime

from django.core import validators
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel

from apps.auto_parks.models import AutoParkModel
from apps.cars.choices.body_type_choices import BodyTypeChoices
from apps.cars.manager import CarManager


class CarModel(BaseModel):
    brand = models.CharField(max_length=25, validators=(
        validators.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg),
    ))
    body = models.CharField(max_length=11, choices=BodyTypeChoices.choices)
    price = models.IntegerField(validators=(
        validators.MinValueValidator(0),
        validators.MaxValueValidator(1000000)
    ))
    year = models.IntegerField(validators=(
        validators.MinValueValidator(1990),
        validators.MaxValueValidator(datetime.now().year)
    ))
    auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')
    objects = models.Manager()
    my_objects = CarManager()

    class Meta:
        db_table = 'cars'
        ordering = ('id',)

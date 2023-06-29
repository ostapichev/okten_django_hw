from django.db import models

from core.models import BaseModel

from .managers import AutoParkManager


class AutoParkModel(BaseModel):
    name = models.CharField(max_length=20)
    objects = AutoParkManager()

    class Meta:
        db_table = 'auto_parks'

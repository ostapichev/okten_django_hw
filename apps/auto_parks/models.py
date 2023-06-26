from django.db import models

from core.models import BaseModel


class AutoParkModel(BaseModel):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'auto_parks'

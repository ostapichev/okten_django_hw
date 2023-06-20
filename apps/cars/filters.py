from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework.serializers import ValidationError

from apps.cars.models import CarModel


def car_filtered_queryset(query: QueryDict) -> QuerySet:
    qs = CarModel.objects.all()
    """
        Розібрати все що було на лекції
        Додати функціонал по видаленню та оновленню автопарків
        До Апки карів додати:
            філтри до кожного поля:
            - для числових (більше менше білше-рівне менше-рівне) 
            -для текстових (починається з, закінчується на, та містить в собі)
            пошук карів по id автопарку через query_params
            а також додати сортування для будь якого поля як ASC так і DESC
    """
    for k, v in query.items():
        match k:
            case 'price_gt':
                qs = qs.filter(price__gt=v)
            case 'price_lt':
                qs = qs.filter(price__lt=v)
            case _:
                raise ValidationError({'detail': f'"{k}" not allowed here'})

    return qs

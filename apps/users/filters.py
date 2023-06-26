from django_filters import rest_framework as filters

from apps.users.models import UserModel


class UserFilter(filters.FilterSet):
    email_start = filters.CharFilter('email', 'istartswith')
    email_contains = filters.CharFilter('email', 'icontains')
    name_contains = filters.CharFilter(field_name='profile__name', lookup_expr='icontains')
    name_start = filters.CharFilter(field_name='profile__name', lookup_expr='istartswith')
    surname_contains = filters.CharFilter(field_name='profile__surname', lookup_expr='icontains')
    surname_start = filters.CharFilter(field_name='profile__surname', lookup_expr='istartswith')


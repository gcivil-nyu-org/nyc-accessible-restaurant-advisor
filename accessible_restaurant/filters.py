import django_filters

from .models import *


class RestaurantFilter(django_filters.FilterSet):
    class Meta:
        model = Restaurant
        fields = []

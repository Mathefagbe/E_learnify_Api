from django_filters import rest_framework as filters
from .models import Course

class CourseFilters(filters.FilterSet):
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['level', 'price_status']
from dataclasses import dataclass

@dataclass
class Review:
    review:str
    rating:int

from typing import Dict
def CardTokenValidation(payload:Review):
   
    print(payload.review)
    print(payload.rating)
   
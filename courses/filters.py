from django_filters import rest_framework as filters
from .models import Course

class CourseFilters(filters.FilterSet):
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    class Meta:
        model = Course
        fields = ['level', 'price_status']





   
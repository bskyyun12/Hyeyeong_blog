from .models import Calendar
import django_filters

class CalendarFilter(django_filters.FilterSet):
    # to make the field case-insensitive
    author__email = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    class Meta:
        model = Calendar
        fields = [
        ]

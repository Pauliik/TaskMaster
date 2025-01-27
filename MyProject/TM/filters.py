import django_filters
from django_filters.widgets import RangeWidget
from django.db.models import Q

from .models import Task, Mytask

#
class Task_filter(django_filters.FilterSet):
    name_task = django_filters.CharFilter(field_name='name_task', lookup_expr='icontains', label="Поиск по заданию")
    due_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['name_task', 'priority', 'status', 'due_date']

#
class Mytask_filter(django_filters.FilterSet):
    text_search = django_filters.CharFilter(method='my_custom_filter', label="Поиск по заданию")
    #name_task = django_filters.CharFilter(field_name='name_task', lookup_expr='icontains')
    due_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = Mytask
        fields = ['text_search', 'priority', 'due_date']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name_task__icontains=value) | Q(description__icontains=value))
    
class Project_filter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Поиск по проекту")
    end_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['name', 'end_date']

class Task_project_filter(django_filters.FilterSet):
    name_task = django_filters.CharFilter(field_name='name_task', lookup_expr='icontains', label="Поиск по заданию")
    due_date = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = Task
        fields = ['name_task', 'priority', 'status', 'executor', 'due_date']
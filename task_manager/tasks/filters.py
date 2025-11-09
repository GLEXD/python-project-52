import django_filters as filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskFilter(filters.FilterSet):
    status = filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус'
    )
    executor = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель'
    )
    label = filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label='Метка'
    )
    self_tasks = filters.BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput,
        method='filter_my_tasks',
    )
    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.label_suffix = ''
        self.form.fields['executor'].label_from_instance = lambda obj: (
            f"{obj.first_name} {obj.last_name}"
        )

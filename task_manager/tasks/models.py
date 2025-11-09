from django.contrib.auth.models import User
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='tasks'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='author'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executor'
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='labels'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

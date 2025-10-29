from django.contrib import admin

from task_manager.labels.models import Label


@admin.register(Label)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name",]
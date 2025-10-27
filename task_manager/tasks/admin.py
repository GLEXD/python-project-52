from django.contrib import admin

from task_manager.tasks.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "author", "executor", "created_at"]
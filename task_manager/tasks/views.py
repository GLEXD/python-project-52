from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class MessageLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect(self.login_url)


class TaskListView(MessageLoginRequiredMixin, FilterView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'task_list'
    filterset_class = TaskFilter


class TaskDetailView(MessageLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'


class TaskCreateView(MessageLoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request,
            'Задача успешно создана'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при создании задачи. Проверьте форму.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': 'Создать задачу',
            'button_action': 'Создать'
        })
        return context


class TaskUpdateView(MessageLoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(
                request,
                'Вы не можете редактировать чужую задачу'
            )
            return redirect('task_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            'Задача успешно изменена'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при изменении задачи. Проверьте форму.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': 'Изменение задачи',
            'button_action': 'Изменить'
        })
        return context


class TaskDeleteView(MessageLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(
                request,
                'Задачу может удалить только ее автор'
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author != request.user:
            messages.error(
                request,
                'Задачу может удалить только ее автор'
            )
            return redirect(self.success_url)

        messages.success(
            request,
            'Задача успешно удалена'
        )
        return self.delete(request, *args, **kwargs)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class MessageLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'home'

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
            )
        return redirect(self.login_url)


class StatusListView(MessageLoginRequiredMixin, ListView):
    model = Status
    template_name = 'status_list.html'
    context_object_name = 'statuses'


class StatusFormMixin:
    form_class = StatusForm
    template_name = 'status_form.html'
    success_url = reverse_lazy('status_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = getattr(
            self,
            'action_label',
            'Изменить'
        )
        context['button_action'] = getattr(
            self,
            'button_label',
            'Сохранить'
        )
        return context


class StatusCreateView(MessageLoginRequiredMixin, StatusFormMixin, CreateView):
    model = Status
    action_label = 'Создать статус'
    button_label = 'Создать'

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при создании статуса. Исправьте ошибки ниже.'
            )
        return super().form_invalid(form)


class StatusUpdateView(MessageLoginRequiredMixin, StatusFormMixin, UpdateView):
    model = Status
    action_label = 'Изменение статуса'
    button_label = 'Изменить'

    def form_valid(self, form):
        messages.success(
            self.request, 'Статус успешно изменена'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при изменении статуса. Исправьте ошибки ниже.'
            )
        return super().form_invalid(form)


class StatusDeleteView(MessageLoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('status_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.error(
                request,
                'Невозможно удалить статус, потому что она используется'
                )
            return redirect(self.success_url)

        messages.success(request, 'Статус успешно удален')
        return self.delete(request, *args, **kwargs)
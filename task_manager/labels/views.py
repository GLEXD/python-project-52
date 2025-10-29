from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class MessageLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'home'

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )
        return redirect(self.login_url)


class LabelListView(MessageLoginRequiredMixin, ListView):
    model = Label
    template_name = 'label_list.html'
    context_object_name = 'labels'


class LabelFormMixin:
    form_class = LabelForm
    template_name = 'label_form.html'
    success_url = reverse_lazy('label_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = getattr(
            self, 'action_label', 'Изменить'
        )
        context['button_action'] = getattr(
            self, 'button_label', 'Сохранить'
        )
        return context


class LabelCreateView(MessageLoginRequiredMixin, LabelFormMixin, CreateView):
    model = Label
    action_label = 'Создать метку'
    button_label = 'Создать'

    def form_valid(self, form):
        messages.success(
            self.request, 'Метка успешно создана'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при создании метки. Исправьте ошибки ниже.'
        )
        return super().form_invalid(form)


class LabelUpdateView(MessageLoginRequiredMixin, LabelFormMixin, UpdateView):
    model = Label
    action_label = 'Изменение метки'
    button_label = 'Изменить'

    def form_valid(self, form):
        messages.success(
            self.request, 'Метка успешно изменена'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при изменении метки. Исправьте ошибки ниже.'
        )
        return super().form_invalid(form)


class LabelDeleteView(MessageLoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('label_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.labels.exists():
            messages.error(
                request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect(self.success_url)

        messages.success(
            request, 'Метка успешно удалена'
        )
        return self.delete(request, *args, **kwargs)
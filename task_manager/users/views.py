from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.models import Task

from .forms import UserForm


class MessageLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'home'

    def handle_no_permission(self):
        messages.error(
                self.request,
                'Вы не авторизованы! Пожалуйста, выполните вход.'
            )
        return redirect(self.login_url)


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user_list'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Пользователь успешно зарегистрирован'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при регистрации. Исправьте ошибки ниже.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': 'Регистрация',
            'button_action': 'Зарегистрировать',
        })
        return context


class UserUpdateView(MessageLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        if str(request.user.pk) != str(kwargs.get('pk')):
            messages.error(
                request,
                'У вас нет прав для изменения другого пользователя.'
            )
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(
            self.request,
            'Пользователь успешно изменен'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Ошибка при изменении пользователя. Исправьте ошибки ниже.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': 'Изменение пользователя',
            'button_action': 'Изменить',
        })
        return context


class UserDeleteView(MessageLoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if str(self.object.pk) != str(request.user.pk):
            messages.error(
                request,
                'У вас нет прав для изменения другого пользователя.'
                )
            return redirect('user_list')
        if Task.objects.filter(author=self.object).exists():
            messages.error(
                request,
                'У вас нет прав для изменения'
            )
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(
            request,
            'Пользователь успешно удален'
        )
        return super().post(request, *args, **kwargs)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при входе. Проверьте данные.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)

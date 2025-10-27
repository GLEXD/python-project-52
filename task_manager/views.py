from django.shortcuts import render, redirect
from django.views import View
from users.models import User


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html')
    def post(self, request, *args, **kwargs):
        return redirect('user_list')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            del request.session['user_id']
        return redirect('home')


class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html', context={'user_list': user_list})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_form.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        return redirect('login')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return render(request, 'login.html', context={'error': 'Invalid data'})

class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('user_list')
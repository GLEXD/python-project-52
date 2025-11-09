"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from task_manager.users.forms import CustomAuthForm
from task_manager.users.views import CustomLoginView, CustomLogoutView

from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('tasks/', include('task_manager.tasks.urls')),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path(
        'login/',
        CustomLoginView.as_view
        (
            template_name='login.html',
            redirect_authenticated_user=True,
            next_page='home',
            authentication_form=CustomAuthForm
        ),
        name='login'
    ),

]

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from users.apps import UsersConfig
from users.views import RegisterView, UserGenericPasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailings:home'), name='logout'),
    path('generate_password/', UserGenericPasswordView.as_view(), name='generate_password'),


]

from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.experiment, name='experiemnt'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('get_name', views.get_user_basic),
    path('get_detail', views.get_user_detail),
]
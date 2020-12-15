from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.experiment, name='experiemnt'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('get_my_info', views.get_my_information),
    path('get_others_info', views.get_others_information),
    path('set_my_info', views.set_my_information),
    path('get_history', views.get_history),
    path('add_fo', views.add_follow),
    path('delete_fo', views.delete_follow),
    path('add_sub', views.add_subscribe),
    path('delete_sub', views.delete_subscribe),
]
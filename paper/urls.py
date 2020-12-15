from django.urls import  path
from . import views
urlpatterns = [
    path('create', views.create_paper),
    path('get', views.get_paper),
    path('set', views.set_info),
    path('add_tag', views.add_tag),
    path('del_tag', views.delete_tag),
]
from django.urls import  path
from . import views
urlpatterns = [
    path('create', views.create_discussion),
    path('get_dis', views.get_discussion),
    path('add_tag', views.add_tag),
    path('del_tag', views.delete_tag),
    path('reply', views.reply),
    path('reco_up', views.reco_up),
    path('reco_down', views.reco_down),
]
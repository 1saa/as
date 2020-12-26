from django.urls import  path
from . import views
urlpatterns = [
    path('papers/', views.search_papers),
    path('discussion/',views.search_discussions),
    path('new_papers/', views.search_new_papers),
    path('new_discussion/', views.search_new_discussions),
    path('hot_discussion/', views.search_hot_discussions),
]
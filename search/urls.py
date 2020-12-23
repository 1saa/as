from django.urls import  path
from . import views
urlpatterns = [
    path('papers/', views.search_papers),
    path('discussion/',views.search_discussions)
]
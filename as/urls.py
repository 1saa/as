"""as URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from search.views import search_results

urlpatterns = [
    path('user_system/', include('user_system.urls')),
    path('discussion/', include('discussion.urls')),
    path('paper/', include('paper.urls')),
    path('admin/', admin.site.urls),
    path('search/', search_results),
] + static('/file/', document_root=settings.MEDIA_ROOT)

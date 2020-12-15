from django.contrib import admin
from .models import User, Discussion, DisCenter, Papers

# Register your models here.
admin.site.register(User)
admin.site.register(Discussion)
admin.site.register(DisCenter)
admin.site.register(Papers)